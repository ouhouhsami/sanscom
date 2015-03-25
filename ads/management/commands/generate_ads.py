#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ads.factories import AdFactory


class Command(BaseCommand):
    args = '<number>'
    help = 'Generate ads'

    def handle(self, *args, **options):
        number = 1000
        if len(args) > 0:
            number = int(args[0])
        AdFactory.create_batch(number)
        #for ad in ads:
        #    AdPictureFactory.create(ad=ad)
        self.stdout.write('Successfully generated items')
