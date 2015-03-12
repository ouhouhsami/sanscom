# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20150304_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='air_conditioning',
            field=models.BooleanField(default=False, verbose_name='Climatisation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='alarm',
            field=models.BooleanField(default=False, verbose_name='Alarme'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='cellar',
            field=models.BooleanField(default=False, verbose_name='Cave'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='digicode',
            field=models.BooleanField(default=False, verbose_name='Digicode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='doorman',
            field=models.BooleanField(default=False, verbose_name='Gardien'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='duplex',
            field=models.BooleanField(default=False, verbose_name='Duplex'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='elevator',
            field=models.BooleanField(default=False, verbose_name='Ascenceur'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Rez de chauss\xe9'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='intercom',
            field=models.BooleanField(default=False, verbose_name='Interphone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='kitchen',
            field=models.BooleanField(default=False, verbose_name='Cuisine \xe9quip\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='not_overlooked',
            field=models.BooleanField(default=False, verbose_name='Sans vis-\xe0-vis'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='separate_dining_room',
            field=models.BooleanField(default=False, verbose_name='Cuisine s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='separate_entrance',
            field=models.BooleanField(default=False, verbose_name='Entr\xe9e s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='swimming_pool',
            field=models.BooleanField(default=False, verbose_name='Piscine'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Dernier \xe9tage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adsearchrelation',
            name='valid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
