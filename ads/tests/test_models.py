#-*- coding: utf-8 -*-
from PIL import Image
import tempfile

from django.core.files import File
from django.test import TestCase

from ads.models import AdPicture
from ads.factories import AdFactory


class AdPictureTestCase(TestCase):

    def test_image_resized(self):
        # Create an Ad
        ad = AdFactory.create()
        # Create an Image
        image = Image.new('RGB', (900, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        ad_picture = AdPicture(ad=ad, title='Foo', image=File(open(tmp_file.name)))
        ad_picture.save()
        # Assert thumbnail are right
        self.assertEqual(ad_picture.image.width, 680)
        self.assertEqual(ad_picture.image.height, 100*680/900)
