#-*- coding: utf-8 -*-
import datetime
import os
import subprocess

from django.core import mail
from django.test import TestCase

from ads.factories import FakeAddressAdFactory
from ads.models import Ad, Search, AdSearchRelation
from ads.tests.utils import search_dict_for_ad


class ChargeTestCase(TestCase):

    fixtures = ['initial-data-load-test.json', ]

    def test_create_a_lot_of_ads(self):
        ads = Ad.objects.all()
        searches = Search.objects.all()
        time_in = datetime.datetime.now()
        # We will update each search to correspond at least to an ad
        for ad in ads:
            search = searches.order_by('?')[0]
            search.__dict__.update(search_dict_for_ad(ad))
            search.save()
            #print len(mail.outbox)
        time_out = datetime.datetime.now()
        print time_out-time_in
        # about 1:21 =>

