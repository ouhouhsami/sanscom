#-*- coding: utf-8 -*-
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry

from ads.factories import AdFactory, SearchFactory
from ads.models import AdSearchRelation, HabitationType
from ads.utils import geo_from_address

from ads.tests.utils import HackyTransactionTestCase, search_for_ad_factory, low_criteria_search_factory, random_habitation_types, random_habitation_type, change_search_to_correspond_to_the_ad, change_search_to_no_more_correspond_to_the_ad


class NotificationTestCase(HackyTransactionTestCase):

    serialized_rollback = True

    def test_ad_then_search(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment, valid=True)
        # Create a search with ad.location inside search.location
        search = search_for_ad_factory(ad)
        # Here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_search_then_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create a search with search.location contaning ad.location
        pnt = GEOSGeometry(geo_from_address("22 rue esquirol Paris"))
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction='sale', valid=True)
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment, transaction=search.transaction, valid=True)
        # here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_ad_then_search_then_update_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment, valid=True)
        pnt = GEOSGeometry(geo_from_address(u"52 W 52nd St, New York, NY 10019, États-Unis"))
        # Create a search with ad.location outside search.location
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction=ad.transaction, valid=True)
        # Here we should have no results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 0)
        search.location = geos.MultiPolygon(ad.location.buffer(2))
        search.save()
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)
        # Then we update the ad
        ad.price = 600001
        ad.save()
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)

    def test_search_then_ad_the_search_update(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create a search with search.location contaning ad.location
        pnt = GEOSGeometry(geo_from_address("22 rue esquirol Paris"))
        search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction='sale', valid=True)
        # Create an ad
        ad = AdFactory(address=u"52 W 52nd St, New York, NY 10019, États-Unis", price=600000, surface=60, habitation_type=apartment, transaction=search.transaction, valid=True)
        # here we should have results ...
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 0)
        ad.address = "22 rue esquirol Paris"
        ad.save()
        #print model_to_dict(search)
        #print model_to_dict(ad)
        self.assertEqual(AdSearchRelation.valid_objects.all().count(), 1)


class MiscellaneousTestCase(HackyTransactionTestCase):

    serialized_rollback = True

    def test_first(self):
        # Create Search
        search = SearchFactory(habitation_types=random_habitation_types(), valid=True)
        # Create Ad
        ad = AdFactory(habitation_type=random_habitation_type(), valid=True)
        # Test if ad is in search (lucky you)
        # We would then modify search so that it doesn't fit anymore
        if AdSearchRelation.valid_objects.all().count() == 1:
            if ad.habitation_type in search.habitation_types.all():
                search.remove(ad.habitation_type)

    def test_second(self):
        # Create ad
        ad = AdFactory(habitation_type=random_habitation_type(), valid=True)
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
