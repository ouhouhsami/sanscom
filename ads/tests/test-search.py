#-*- coding: utf-8 -*-
from django.contrib.gis import geos
from django.contrib.sites.models import get_current_site
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import AnonymousUser, User
from django.core import mail
from django.forms.models import model_to_dict
from django.http import Http404, QueryDict
from django.test import TestCase, RequestFactory

from ads.factories import AdFactory, SearchFactory
from ads.forms import SearchSearchForm
from ads.models import HabitationType, Search
from ads.utils import geo_from_address
from ads.views import SearchDetailView, DeleteSearchView, CreateSearchView, SearchListView

from .utils import add_namespace_to_request, none_to_empty_string, add_session_to_request, low_criteria_search_factory

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
