import unittest

from django.test import Client
from django.core.urlresolvers import reverse

from ads.factories import AdFactory


class ReachStaticPages(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_reach_about(self):
        response = self.client.get(reverse('a-propos'))
        self.assertEqual(response.status_code, 200)

    def test_reach_legal(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)

    def test_reach_cgu(self):
        response = self.client.get(reverse('cgu'))
        self.assertEqual(response.status_code, 200)


class ReachSaleAndRentPages(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_reach_ad_list_no_logged(self):
        response = self.client.get(reverse('sale:ads_ad_list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rent:ads_ad_list'))
        self.assertEqual(response.status_code, 200)

    def test_reach_ad_add_not_logged(self):
        response = self.client.get(reverse('sale:ads_ad_add'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rent:ads_ad_add'))
        self.assertEqual(response.status_code, 200)

    def test_reach_ad_detail_not_logged(self):
        ad = AdFactory.create(transaction="sale")
        response = self.client.get(reverse('sale:ads_ad_detail', kwargs={'slug':ad.slug}))
        self.assertEqual(response.status_code, 200)
        ad = AdFactory.create(transaction="rent")
        response = self.client.get(reverse('rent:ads_ad_detail', kwargs={'slug':ad.slug}))
        self.assertEqual(response.status_code, 200)

    def test_reach_ad_update_sale(self):
        ad = AdFactory.create(transaction="sale")
        response = self.client.get(reverse('sale:ads_ad_update', kwargs={'slug':ad.slug}))
        self.assertEqual(response.status_code, 302) # Redirection as user not logged
        user = ad.user
        user.set_password('coucou')
        user.save()
        self.client.login(username=ad.user.username, password='coucou')
        response = self.client.get(reverse('sale:ads_ad_update', kwargs={'slug':ad.slug}))
        self.assertEqual(response.status_code, 200)

    def test_reach_ad_update_rent(self):
        rent = AdFactory.create(transaction="rent")
        response = self.client.get(reverse('rent:ads_ad_update', kwargs={'slug':rent.slug}))
        self.assertEqual(response.status_code, 302) # Redirection as user not logged
        user = rent.user
        user.set_password('coucou')
        user.save()
        self.client.login(username=rent.user.username, password='coucou')
        response = self.client.get(reverse('rent:ads_ad_update', kwargs={'slug':rent.slug}))
        self.assertEqual(response.status_code, 200)
