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

# CRUD Ads
class ReadAdsViewTestCase(TestCase):

    def test_ad_read_anonymous_user(self):
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), False)

    def test_ad_read_logged_user_no_adsearch_for_ad(self):
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = User.objects.create_user(
            username='jacob', email='jacob@cool.net', password='top_secret')
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), False)

    def test_ad_read_logged_user_adsearch_for_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment)
        pnt = GEOSGeometry(geo_from_address(u"22 rue esquirol Paris"))
        # Create a search with ad.location inside search.location
        ad_search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction=ad.transaction)

        # Here, 2 mails should have been sent
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].recipients()[0], ad.user.email)
        self.assertEqual(mail.outbox[1].recipients()[0], ad_search.user.email)
        ad_search_full_url = u''.join(['http://', get_current_site(None).domain, ad_search.get_absolute_url()])
        ad_full_url = u''.join(['http://', get_current_site(None).domain, ad.get_absolute_url()])
        self.assertTrue(ad_search_full_url.encode('utf8') in mail.outbox[0].message().as_string())
        self.assertTrue(ad_full_url.encode('utf8') in mail.outbox[1].message().as_string())

        request = RequestFactory().get('/fake-path')
        request.user = ad_search.user
        add_namespace_to_request(request, ad_search)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), True)
        # We should then be able to contact the vendor
        request = RequestFactory().post('/fake-path', {'message': 'hi there'})
        request.user = ad_search.user
        add_namespace_to_request(request, ad_search)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(mail.outbox[2].body, 'hi there')
        # Now, when reach web page, the user should know that he has already contacted the vendor
        request = RequestFactory().get('/fake-path')
        request.user = ad_search.user
        add_namespace_to_request(request, ad_search)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.context_data.has_key('already_contacted'), True)


class CreateAdsViewTestCase(TestCase):

    def test_ad_create_logged_user(self):
        # Get the view
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        # Prepare data for the form (from the valid ad created at the begining)
        ad_dict = none_to_empty_string(model_to_dict(ad, exclude=('id', 'location')))
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        formset_data = {
            'adpicture_set-TOTAL_FORMS': u'4',
            'adpicture_set-INITIAL_FORMS': u'0',
            'adpicture_set-MAX_NUM_FORMS': u'4',
            'adpicture_set-0-title': 'Le salon',
            'adpicture_set-0-image': open(tmp_file.name, "r")
        }
        ad_dict.update(formset_data)
        request = RequestFactory().post('/fake-path', ad_dict, format="multipart")
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        # This is a redirection when form is valid
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Ad.objects.all()[1].get_absolute_url())
        # We now have 2 ads: one we used to create valid data, and the ad created with POST method just above
        self.assertEqual(len(Ad.objects.all()), 2)
        # Check that image is saved too
        self.assertEqual(len(Ad.objects.all()[1].adpicture_set.all()), 1)

        # here we update with more picture
        # and it works
        ad_dict['price'] = 200
        ad_dict['adpicture_set-0-image'] = open(tmp_file.name, "r")
        request = RequestFactory().post('/fake-path', ad_dict, format="multipart")
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = UpdateAdView.as_view()
        response = view(request, slug=ad.slug)

    def test_ad_create_not_logged_user(self):
        # Get the view
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        ad_dict = none_to_empty_string(model_to_dict(ad, exclude=('id', 'location')))

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        formset_data = {
            'adpicture_set-TOTAL_FORMS': u'4',
            'adpicture_set-INITIAL_FORMS': u'0',
            'adpicture_set-MAX_NUM_FORMS': u'4',
            'adpicture_set-0-title': 'Le salon',
            'adpicture_set-0-image': open(tmp_file.name, "r")
        }
        ad_dict.update(formset_data)
        user_credentials = {
            'username': 'ouhouhsami',
            'email': 'ouhouhsami@achetersanscom.com',
            'password': '1234',
            'password2': '1234'
        }
        ad_dict.update(user_credentials)
        request = RequestFactory().post('/fake-path', ad_dict, format="multipart")
        request.user = AnonymousUser()
        add_session_to_request(request) # Trick to add session even with an anonyomous user and RequestFactory
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Ad.objects.all()[1].get_absolute_url())
        # Test that create ad belongs to the newly registered user
        self.assertEqual(Ad.objects.all()[1].user.username, user_credentials['username'])
        # Test that picture is also saved with the ad
        self.assertEqual(len(Ad.objects.all()[1].adpicture_set.all()), 1)
        self.assertEqual(len(Ad.objects.all()), 2)

    def test_ad_create_not_logged_user_but_having_username(self):
        # Get the view
        ad = AdFactory.create()
        username = "sam"
        password = "gld"
        user = User.objects.create_user(
            username=username, email='jacob@cool.net', password=password)
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        ad_dict = none_to_empty_string(model_to_dict(ad, exclude=('id', 'location')))

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        formset_data = {
            'adpicture_set-TOTAL_FORMS': u'4',
            'adpicture_set-INITIAL_FORMS': u'0',
            'adpicture_set-MAX_NUM_FORMS': u'4',
            'adpicture_set-0-title': 'Le salon',
            'adpicture_set-0-image': open(tmp_file.name, "r")
        }
        ad_dict.update(formset_data)
        user_credentials = {
            'login_username': username,
            'login_password': password
        }
        ad_dict.update(user_credentials)
        request = RequestFactory().post('/fake-path', ad_dict, format="multipart")
        request.user = AnonymousUser()
        add_session_to_request(request) # Trick to add session even with an anonyomous user and RequestFactory
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        # Redirection
        self.assertEqual(response.status_code, 302)
        created_ad = Ad.objects.get(user=user)
        self.assertEqual(response.url, created_ad.get_absolute_url())
        # Test that picture is also saved with the ad
        self.assertEqual(len(created_ad.adpicture_set.all()), 1)
        self.assertEqual(len(Ad.objects.all()), 2)


class UpdateAdsViewTestCase(TestCase):

    def test_ad_update(self):
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = UpdateAdView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)

        ad_dict = none_to_empty_string(model_to_dict(ad, exclude=('id', 'location')))
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        formset_data = {
            'adpicture_set-TOTAL_FORMS': u'4',
            'adpicture_set-INITIAL_FORMS': u'0',
            'adpicture_set-MAX_NUM_FORMS': u'4',
            'adpicture_set-0-title': 'Le salon',
            'adpicture_set-0-image': open(tmp_file.name, "r")
        }
        ad_dict.update(formset_data)
        new_price = 200
        ad_dict['price'] = new_price
        request = RequestFactory().post('/fake-path', ad_dict, format="multipart")
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = UpdateAdView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(len(Ad.objects.all()), 1)
        self.assertEqual(Ad.objects.all()[0].price, new_price)


class DeleteAdsViewTestCase(TestCase):

    def test_ad_delete_for_the_owner(self):
        # Reach delete page
        ad = AdFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = DeleteAdView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        # Delete ad
        request = RequestFactory().post('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = DeleteAdView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(len(Ad.objects.all()), 0)

    def test_ad_delete_if_user_not_owner(self):
        ad = AdFactory.create()
        not_owner = User.objects.create_user(
            username='jacob', email='jacob@cool.net', password='top_secret')
        request = RequestFactory().get('/fake-path')
        request.user = not_owner
        add_namespace_to_request(request, ad)
        self.assertRaises(Http404, DeleteAdView.as_view(), request, slug=ad.slug)
        request = RequestFactory().post('/fake-path')
        request.user = not_owner
        add_namespace_to_request(request, ad)
        self.assertRaises(Http404, DeleteAdView.as_view(), request, slug=ad.slug)


class AdListViewTestCase(TestCase):

    def test_reach_list_view(self):
        # empty db, just reach home page
        request = RequestFactory().get('/fake-path')
        add_namespace_to_request(request, 'sale')
        view = AdListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['form'].__class__ == SearchAdForm)
        self.assertTrue(response.context_data['valid'] == False)

    def test_create_search_from_ad_list(self):
        # need to have a clean search
        search = SearchFactory.create(habitation_types = HabitationType.objects.all())
        search_dict = none_to_empty_string(model_to_dict(search, exclude=('id')))
        search_dict['location'] = search_dict['location'].geojson
        search_dict['save_ad'] = True
        request = RequestFactory().get('/fake-path', search_dict)
        add_namespace_to_request(request, search)
        view = AdListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        params = QueryDict(response.url.split('?')[1])
        self.assertEqual(int(params['price_max']), search_dict['price_max'])
        self.assertEqual(int(params['surface_min']), search_dict['surface_min'])
        self.assertEqual(int(params['rooms_min']), search_dict['rooms_min'])
        self.assertEqual(params['location'], str(search_dict['location']))
        self.assertEqual(map(lambda x: int(x), params.getlist('habitation_types')), search_dict['habitation_types'])


# CRUD Search

class CreateSearchViewTestCase(TestCase):

    def test_search_create_logged_user(self):
        # Get the view
        search = SearchFactory.create(habitation_types = HabitationType.objects.all())
        #print search.__dict__
        request = RequestFactory().get('/fake-path')
        request.user = search.user
        add_namespace_to_request(request, search)
        view = CreateSearchView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        # Prepare data for the form (from the valid ad created at the begining)
        search_dict = none_to_empty_string(model_to_dict(search, exclude=('id')))
        #search_dict = {key: (value if value is not None else "") for key, value in search_dict.items()}
        search_dict['location'] = search_dict['location'].geojson
        request = RequestFactory().post('/fake-path', search_dict)
        request.user = search.user
        add_namespace_to_request(request, search)
        view = CreateSearchView.as_view()
        response = view(request)
        # This is a redirection when form is valid
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Search.objects.exclude(id=search.id).get(user=search.user).get_absolute_url())

    def test_search_create_not_logged_user(self):
        # Get the view
        search = SearchFactory.create(habitation_types = HabitationType.objects.all())
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, search)
        view = CreateSearchView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        search_dict = none_to_empty_string(model_to_dict(search, exclude=('id')))
        search_dict['location'] = search_dict['location'].geojson

        user_credentials = {
            'username': 'ouhouhsami',
            'email': 'ouhouhsami@achetersanscom.com',
            'password': '1234',
            'password2': '1234'
        }

        search_dict.update(user_credentials)
        request = RequestFactory().post('/fake-path', search_dict, format="multipart")
        request.user = AnonymousUser()
        add_namespace_to_request(request, search)
        add_session_to_request(request) # Trick to add session even with an anonyomous user and RequestFactory
        view = CreateSearchView.as_view()
        response = view(request)
        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Search.objects.get(user__username=search_dict['username']).get_absolute_url())
        # Test that create ad belongs to the newly registered user
        self.assertEqual(Search.objects.get(user__username=search_dict['username']).user.username, user_credentials['username'])

    def test_search_create_not_logged_user_but_having_username(self):
       # Get the view
        search = SearchFactory.create(habitation_types = HabitationType.objects.all())
        username = "sam"
        password = "gld"
        user = User.objects.create_user(
            username=username, email='jacob@cool.net', password=password)
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, search)
        view = CreateSearchView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        search_dict = none_to_empty_string(model_to_dict(search, exclude=('id')))
        search_dict['location'] = search_dict['location'].geojson

        user_credentials = {
            'login_username': username,
            'login_password': password
        }
        search_dict.update(user_credentials)
        request = RequestFactory().post('/fake-path', search_dict, format="multipart")
        request.user = AnonymousUser()
        add_session_to_request(request) # Trick to add session even with an anonyomous user and RequestFactory
        add_namespace_to_request(request, search)
        view = CreateSearchView.as_view()
        response = view(request)
        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Search.objects.exclude(id=search.id).get(user__username=search_dict['login_username']).get_absolute_url())
        # Test that create ad belongs to the newly registered user
        self.assertEqual(Search.objects.exclude(id=search.id).get(user__username=search_dict['login_username']).user.username, user_credentials['login_username'])


class ReadSearchViewTestCase(TestCase):

    def test_search_read_anonymous_user(self):
        search = SearchFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, search)
        view = SearchDetailView.as_view()
        response = view(request, slug=search.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), False)

    def test_search_read_logged_user_no_ad_for_search(self):
        search = SearchFactory.create()
        request = RequestFactory().get('/fake-path')
        request.user = User.objects.create_user(
            username='jacob', email='jacob@cool.net', password='top_secret')
        add_namespace_to_request(request, search)
        view = SearchDetailView.as_view()
        response = view(request, slug=search.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), False)

    def test_search_read_logged_user_ad_for_search(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment)
        pnt = GEOSGeometry(geo_from_address(u"22 rue esquirol Paris"))
        # Create a search with ad.location inside search.location
        ad_search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction=ad.transaction)

        # Here, 2 mails should have been sent
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].recipients()[0], ad.user.email)
        self.assertEqual(mail.outbox[1].recipients()[0], ad_search.user.email)
        ad_search_full_url = u''.join(['http://', get_current_site(None).domain, ad_search.get_absolute_url()])
        ad_full_url = u''.join(['http://', get_current_site(None).domain, ad.get_absolute_url()])
        self.assertTrue(ad_search_full_url.encode('utf8') in mail.outbox[0].message().as_string())
        self.assertTrue(ad_full_url.encode('utf8') in mail.outbox[1].message().as_string())


        request = RequestFactory().get('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = SearchDetailView.as_view()
        response = view(request, slug=ad_search.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.has_key('contact_form'), True)
        # We should then be able to contact the vendor
        request = RequestFactory().post('/fake-path', {'message': 'hi there'})
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = SearchDetailView.as_view()
        response = view(request, slug=ad_search.slug)
        self.assertEqual(mail.outbox[2].body, 'hi there')
        # Now, when reach web page, the user should know that he has already contacted the vendor
        request = RequestFactory().get('/fake-path')
        request.user = ad.user
        add_namespace_to_request(request, ad)
        view = SearchDetailView.as_view()
        response = view(request, slug=ad_search.slug)
        self.assertEqual(response.context_data.has_key('already_contacted'), True)


class DeleteSearchViewTestCase(TestCase):

    def test_search_delete_for_the_owner(self):
        search = SearchFactory.create()
        self.assertEqual(len(Search.objects.all()), 1)
        request = RequestFactory().get('/fake-path')
        request.user = search.user
        add_namespace_to_request(request, search)
        view = DeleteSearchView.as_view()
        response = view(request, slug=search.slug)
        self.assertEqual(response.status_code, 200)
        # Delete ad
        request = RequestFactory().post('/fake-path')
        request.user = search.user
        add_namespace_to_request(request, search)
        view = DeleteSearchView.as_view()
        response = view(request, slug=search.slug)
        self.assertEqual(len(Search.objects.all()), 0)

    def test_search_delete_if_user_not_the_owner(self):
        search = SearchFactory.create()
        not_owner = User.objects.create_user(
            username='jacob', email='jacob@cool.net', password='top_secret')
        self.assertEqual(len(Search.objects.all()), 1)
        request = RequestFactory().get('/fake-path')
        request.user = not_owner
        add_namespace_to_request(request, search)
        view = DeleteSearchView.as_view()
        self.assertRaises(Http404, view, request, slug=search.slug)
        # Delete search
        request = RequestFactory().post('/fake-path')
        request.user = not_owner
        add_namespace_to_request(request, search)
        view = DeleteSearchView.as_view()
        self.assertRaises(Http404, view, request, slug=search.slug)
        self.assertEqual(len(Search.objects.all()), 1)


class SearchListViewTestCase(TestCase):

    def test_reach_list_view(self):
        # empty db, just reach home page
        request = RequestFactory().get('/fake-path')
        add_namespace_to_request(request, 'sale')
        view = SearchListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['form'].__class__ == SearchSearchForm)
        self.assertTrue(response.context_data['valid'] == False)

    def test_create_ad_from_ad_list(self):
        # need to have a clean search
        ad = AdFactory.create()
        ad_dict = none_to_empty_string(model_to_dict(ad, exclude=('id', 'location')))
        ad_dict['address'] = ad_dict['address']
        ad_dict['save_ad'] = True
        request = RequestFactory().get('/fake-path', ad_dict)
        add_namespace_to_request(request, ad)
        view = SearchListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        params = QueryDict(response.url.split('?')[1])
        self.assertEqual(int(params['price']), ad_dict['price'])
        self.assertEqual(int(params['surface']), ad_dict['surface'])
        #@todo test location and habitation_type
        #self.assertEqual(params['location'], str(ad_dict['location']))
        self.assertEqual(int(params.get('habitation_type')), ad_dict['habitation_type'])

# Link between Ads and Search

class NotificationTestCase(HackyTransactionTestCase):

    serialized_rollback = True

    def test_ad_then_search(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment)
        # Create a search with ad.location inside search.location
        search = search_for_ad_factory(ad)
        # Here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_search_then_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create a search with search.location contaning ad.location
        pnt = GEOSGeometry(geo_from_address("22 rue esquirol Paris"))
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction='sale')
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment, transaction=search.transaction)
        # here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_ad_then_search_then_update_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment)
        pnt = GEOSGeometry(geo_from_address(u"52 W 52nd St, New York, NY 10019, États-Unis"))
        # Create a search with ad.location outside search.location
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction=ad.transaction)
        # here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 0)

        search.location = geos.MultiPolygon(ad.location.buffer(2))
        search.save()
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_search_then_ad_the_search_update(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create a search with search.location contaning ad.location
        pnt = GEOSGeometry(geo_from_address("22 rue esquirol Paris"))
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction='sale')
        # Create an ad
        ad = AdFactory(address=u"52 W 52nd St, New York, NY 10019, États-Unis", price=600000, surface=60, habitation_type=apartment, transaction=search.transaction)
        # here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 0)
        ad.address = "22 rue esquirol Paris"
        ad.save()
        #print model_to_dict(search)
        #print model_to_dict(ad)
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)


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


class MiscellaneousTestCase(HackyTransactionTestCase):

    serialized_rollback = True

    def test_first(self):
        # Create Search
        search = SearchFactory(habitation_types=random_habitation_types())
        # Create Ad
        ad = AdFactory(habitation_type=random_habitation_type())
        # Test if ad is in search (lucky you)
        # We would then modify search so that it doesn't fit anymore
        if AdSearchRelation.valid_objects.all().count() == 1:
            if ad.habitation_type in search.habitation_types.all():
                search.remove(ad.habitation_type)

    def test_second(self):
        # Create ad
        ad = AdFactory(habitation_type=random_habitation_type())
        # Check AdSearchRelation is empty
        self.assertEqual(AdSearchRelation.valid_objects.count(), 0)
        # Create search which corresponds to an add
        search = search_for_ad_factory(ad)
        # Test that it there is a ASR for ad <=> search
        # self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)
        change_search_to_no_more_correspond_to_the_ad(search, ad)
        self.assertEqual(AdSearchRelation.valid_objects.count(), 0)
        change_search_to_correspond_to_the_ad(search, ad)
        self.assertEqual(AdSearchRelation.valid_objects.count(), 1)

