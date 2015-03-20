from django.core.management.base import BaseCommand, CommandError
from ads.factories import AdFactory, SearchFactory, AccountFactory, AdPictureFactory, HabitationTypeFactory
from ads.models import HabitationType

class Command(BaseCommand):
    args = '<ads_number>'
    help = 'Generate random data for ads and search'

    def handle(self, *args, **options):
        number = 10
        if len(args) > 0:
            number = int(args[0])
        #HabitationTypeFactory.create_batch(2)
        # AccountFactory.create_batch(number)
        # ads = AdFactory.create_batch(number)
        # for ad in ads:
        #     AdPictureFactory.create(ad=ad)
        #     AdPictureFactory.create(ad=ad)
        SearchFactory.create_batch(number, habitation_types=[HabitationType.objects.all().order_by('?')[0]])
        self.stdout.write('Successfully generated items')
