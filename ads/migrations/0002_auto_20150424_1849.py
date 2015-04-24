# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_squashed_0002_auto_20150407_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='valid',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='valid',
            field=models.NullBooleanField(),
            preserve_default=True,
        )
    ]
