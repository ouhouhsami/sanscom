#-*- coding: utf-8 -*-
import datetime
import os
import subprocess

from django.test import TestCase

from ads.factories import FakeAddressAdFactory

from ads.tests.utils import search_for_ad_factory


class ChargeTestCase(TestCase):

    def test_create_a_lot_of_ads(self):
        # Seloger has 22123 ads in Paris
        # so we create the same number of ads
        time_in = datetime.datetime.now()
        ads = FakeAddressAdFactory.create_batch(100, transaction='sale')
        for ad in ads:
            search_for_ad_factory(ad)
        time_out = datetime.datetime.now()
        bkp_file = 'test_charge.sql'
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), bkp_file)
        #dumper_cmd = ['pg_dump', '-h', localhost, '-p', port, '-U', db_username, '--role', role, '-W', '-Fc', '-v', '-f', file_path, db_name]
        dumper_cmd = ['pg_dump', '-a', '-f', file_path, 'test_sanscom']
        subprocess.check_output(dumper_cmd)
        print time_out-time_in
        self.assertEqual(True, True)

