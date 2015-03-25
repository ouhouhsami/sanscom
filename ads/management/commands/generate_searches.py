#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ads.factories import AdFactory, SearchFactory, AccountFactory, AdPictureFactory, HabitationTypeFactory
from ads.models import HabitationType


class Command(BaseCommand):
    args = '<number>'
    help = 'Generate searches'

    def handle(self, *args, **options):
        number = 1000
        SearchFactory.create_batch(number, habitation_types=[HabitationType.objects.all().order_by('?')[0]])
        self.stdout.write('Successfully generated searches')
