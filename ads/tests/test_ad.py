#-*- coding: utf-8 -*-
from PIL import Image
import tempfile

from django.contrib.gis import geos
from django.contrib.sites.models import get_current_site
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import AnonymousUser, User
from django.core import mail
from django.forms.models import model_to_dict
from django.http import Http404, QueryDict
from django.test import TestCase, RequestFactory

from ads.factories import AdFactory, SearchFactory
from ads.forms import SearchAdForm
from ads.models import HabitationType, Ad
from ads.utils import geo_from_address
from ads.views import AdDetailView, CreateAdView, UpdateAdView, DeleteAdView, AdListView

from ads.tests.utils import add_namespace_to_request, low_criteria_search_factory, none_to_empty_string, add_session_to_request


class ReadAdsViewTestCase(TestCase):

    def test_anonymous_user_valid_ad(self):
        ad = AdFactory.create(valid=True)
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contact_form' in response.context_data)

    def test_anonymous_user_invalid_ad(self):
        ad = AdFactory.create(valid=False)
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        self.assertRaises(Http404, view, request, slug=ad.slug)

    def test_anonymous_user_not_valided_ad(self):
        ad = AdFactory.create()  # valid is set to None by default
        request = RequestFactory().get('/fake-path')
        request.user = AnonymousUser()
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        self.assertRaises(Http404, view, request, slug=ad.slug)

    def test_logged_user_no_adsearch_for_ad(self):
        ad = AdFactory.create(valid=True)
        request = RequestFactory().get('/fake-path')
        request.user = User.objects.create_user(
            username='jacob', email='jacob@cool.net', password='top_secret')
        add_namespace_to_request(request, ad)
        view = AdDetailView.as_view()
        response = view(request, slug=ad.slug)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contact_form' in response.context_data)

    def test_logged_user_adsearch_for_ad(self):
        house, create = HabitationType.objects.get_or_create(label="Maison")
        apartment, create = HabitationType.objects.get_or_create(label="Appartement")
        # Create an ad
        ad = AdFactory(address="22 rue esquirol Paris", price=600000, surface=60, habitation_type=apartment, valid=True)
        pnt = GEOSGeometry(geo_from_address(u"22 rue esquirol Paris"))
        # Create a search with ad.location inside search.location
        ad_search = low_criteria_search_factory(location=geos.MultiPolygon(pnt.buffer(2)), price_max=700000, surface_min=50, habitation_types=[apartment, ], transaction=ad.transaction, valid=True)

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
        self.assertTrue('contact_form' in response.context_data)
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
        self.assertTrue('already_contacted' in response.context_data)


class CreateAdsViewTestCase(TestCase):

    def test_logged_user(self):
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

    def test_not_logged_user(self):
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
        add_session_to_request(request)  # Trick to add session even with an anonyomous user and RequestFactory
        add_namespace_to_request(request, ad)
        view = CreateAdView.as_view()
        response = view(request)
        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, Ad.objects.filter(user=User.objects.get(username="ouhouhsami"))[0].get_absolute_url())
        # Test that picture is also saved with the ad
        self.assertEqual(len(Ad.objects.filter(user=User.objects.get(username="ouhouhsami"))[0].adpicture_set.all()), 1)
        self.assertEqual(len(Ad.objects.all()), 2)

    def test_not_logged_user_but_having_username(self):
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
        add_session_to_request(request)  # Trick to add session even with an anonyomous user and RequestFactory
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
        image = Image.new('RGB', (800, 100))
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
        self.assertTrue(response.context_data['valid'] is False)

    def test_create_search_from_ad_list(self):
        # need to have a clean search
        search = SearchFactory.create(habitation_types=HabitationType.objects.all())
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
