# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_auto_20150312_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='rooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nb de pi\xe8ce minimum', blank=True),
            preserve_default=True,
        ),
    ]
