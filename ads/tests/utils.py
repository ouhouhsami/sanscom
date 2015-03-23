#-*- coding: utf-8 -*-
from PIL import Image
import tempfile
from mock import Mock

from django.test import TransactionTestCase, TestCase, RequestFactory
from django.contrib.gis import geos
from django.contrib.sites.models import get_current_site
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import AnonymousUser, User
from django.forms.models import model_to_dict
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404, QueryDict

from .factories import AdFactory, SearchFactory, HabitationType
from .models import AdSearchRelation, HabitationType, Ad, Search
from .utils import geo_from_address, address_from_geo
from .views import AdDetailView, CreateAdView, UpdateAdView, DeleteAdView, SearchDetailView, DeleteSearchView, CreateSearchView, UpdateSearchView, AdListView, SearchListView
from .forms import EditAdForm, SearchAdForm, SearchSearchForm

# Hacky part
#SEE https://code.djangoproject.com/ticket/23727
from django.apps import apps
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.auth.management import create_permissions
from django.contrib.sites.management import create_default_site
from django.db.models import signals
from django.core import mail


def update_group_permissions(sender, **kwargs):
    if unicode(sender).find("django.contrib.auth.models") != -1:
        for group_name in group_perms.keys():
            group = Group.objects.get(name=group_name)
            for perm_codename in group_perms[group_name]['perms']:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            group.save()


class HackyTransactionTestCase(TransactionTestCase):
    def _fixture_setup(self):
        super(HackyTransactionTestCase, self)._fixture_setup()
        for app_config in apps.get_app_configs():
            update_contenttypes(app_config)
            create_permissions(app_config)
            create_default_site(app_config)

    def _fixture_teardown(self):
        signals.post_migrate.disconnect(create_default_site, sender=apps.get_app_config('sites'))
        signals.post_migrate.disconnect(update_contenttypes)
        signals.post_migrate.disconnect(create_permissions, dispatch_uid="django.contrib.auth.management.create_permissions")
        signals.post_migrate.disconnect(update_group_permissions)

        super(HackyTransactionTestCase, self)._fixture_teardown()

        signals.post_migrate.connect(update_contenttypes)
        signals.post_migrate.connect(create_permissions, dispatch_uid="django.contrib.auth.management.create_permissions")
        signals.post_migrate.connect(create_default_site, sender=apps.get_app_config('sites'))
# End of hacky part

# Hacky part - part 2
def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
# End of hacky part 2

# To get a clean dictionnary from a model instance
# which will transform None to empty string

def none_to_empty_string(dict):
    return {key: (value if value is not None else "") for key, value in dict.items()}


def add_namespace_to_request(request, item):
    request.resolver_match = Mock()
    if isinstance(item, basestring):
        request.resolver_match.namespace = item
    else:
        request.resolver_match.namespace = item.transaction

import random


def random_habitation_types():
    r = random.randint(0, 2)
    house, create = HabitationType.objects.get_or_create(label="Maison")
    apartment, create = HabitationType.objects.get_or_create(label="Appartement")
    if r == 0:
        return [apartment]
    elif r == 1:
        return [house]
    elif r == 2:
        return [apartment, house]


def random_habitation_type():
    r = random.randint(0, 1)
    house, create = HabitationType.objects.get_or_create(label="Maison")
    apartment, create = HabitationType.objects.get_or_create(label="Appartement")
    if r == 1:
        return apartment
    else:
        return house


def low_criteria_search_factory(location, price_max, surface_min, habitation_types, transaction):
    return SearchFactory(location=location, price_max=price_max, surface_min=surface_min, habitation_types=habitation_types, transaction=transaction,
        rooms_min = None,
        bedrooms_min = None,
        ground_surface_min = None,
        ground_floor = None,
        top_floor = None,
        not_overlooked = None,
        elevator = None,
        intercom = None,
        digicode = None,
        doorman = None,
        kitchen = None,
        duplex = None,
        swimming_pool = None,
        alarm = None,
        air_conditioning = None,
        fireplace = None,
        terrace = None,
        balcony = None,
        separate_dining_room = None,
        separate_toilet = None,
        bathroom = None,
        shower = None,
        separate_entrance = None,
        cellar = None,
        parking = None)


def search_for_ad_factory(ad):
    search = SearchFactory(
        transaction = ad.transaction,
        location=geos.MultiPolygon(ad.location.buffer(2)),
        surface_min = ad.surface,
        rooms_min = ad.rooms,
        price_max = ad.price,
        habitation_types=[ad.habitation_type, ],
        bedrooms_min = ad.bedrooms,
        ground_surface_min = ad.ground_surface,
        ground_floor = None,
        top_floor = None,
        not_overlooked = None,
        elevator = None,
        intercom = None,
        digicode = None,
        doorman = None,
        kitchen = None,
        duplex = None,
        swimming_pool = None,
        alarm = None,
        air_conditioning = None,
        fireplace = None,
        terrace = None,
        balcony = None,
        separate_dining_room = None,
        separate_toilet = None,
        bathroom = None,
        shower = None,
        separate_entrance = None,
        cellar = None,
        parking = None
    )
    return search


def change_search_to_no_more_correspond_to_the_ad(search, ad):
    search.rooms_min = ad.rooms + 1
    search.save()

def change_search_to_correspond_to_the_ad(search, ad):
    search.rooms_min = ad.rooms
    search.save()
