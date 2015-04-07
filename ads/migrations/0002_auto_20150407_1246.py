# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_squashed_0008_auto_20150321_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='json_address',
            field=jsonfield.fields.JSONField(default='{}'),
            preserve_default=False,
        )
    ]
