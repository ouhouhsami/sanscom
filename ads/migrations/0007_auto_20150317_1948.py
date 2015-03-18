# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_search_rooms_min'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='air_conditioning',
            field=models.NullBooleanField(verbose_name='Climatisation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='alarm',
            field=models.NullBooleanField(verbose_name='Alarme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='balcony',
            field=models.NullBooleanField(verbose_name='Balcon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='bathroom',
            field=models.NullBooleanField(verbose_name='Salle de bain'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='bedrooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nombre de chambres minimum', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='cellar',
            field=models.NullBooleanField(verbose_name='Cave'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='digicode',
            field=models.NullBooleanField(verbose_name='Digicode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='doorman',
            field=models.NullBooleanField(verbose_name='Gardien'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='duplex',
            field=models.NullBooleanField(verbose_name='Duplex'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='elevator',
            field=models.NullBooleanField(verbose_name='Ascenceur'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='fireplace',
            field=models.NullBooleanField(verbose_name='Chemin\xe9e'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='ground_floor',
            field=models.NullBooleanField(verbose_name='Rez de chauss\xe9'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='ground_surface_min',
            field=models.IntegerField(null=True, verbose_name='Surface du terrain minimale', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='intercom',
            field=models.NullBooleanField(verbose_name='Interphone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='kitchen',
            field=models.NullBooleanField(verbose_name='Cuisine \xe9quip\xe9e'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='not_overlooked',
            field=models.NullBooleanField(verbose_name='Sans vis-\xe0-vis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='parking',
            field=models.NullBooleanField(verbose_name='Parking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_dining_room',
            field=models.NullBooleanField(verbose_name='Cuisine s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_entrance',
            field=models.NullBooleanField(verbose_name='Entr\xe9e s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_toilet',
            field=models.NullBooleanField(verbose_name='Toilettes s\xe9par\xe9s'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='shower',
            field=models.NullBooleanField(verbose_name="Salle d'eau (douche)"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='swimming_pool',
            field=models.NullBooleanField(verbose_name='Piscine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='terrace',
            field=models.NullBooleanField(verbose_name='Terrasse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='top_floor',
            field=models.NullBooleanField(verbose_name='Dernier \xe9tage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='rooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nb de pi\xe8ces minimum', blank=True),
            preserve_default=True,
        ),
    ]
