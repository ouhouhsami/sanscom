# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_auto_20150312_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Localisation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='location',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='Localisation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='price_max',
            field=models.PositiveIntegerField(verbose_name='Prix maximum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='surface_min',
            field=models.PositiveIntegerField(verbose_name='Surface minimale'),
            preserve_default=True,
        ),
    ]
