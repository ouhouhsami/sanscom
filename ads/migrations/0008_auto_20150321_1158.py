# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ads.models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_auto_20150317_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='transaction',
            field=models.CharField(default='sale', max_length=4, choices=[(b'sale', 'Vente'), (b'rent', 'Location')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='transaction',
            field=models.CharField(default='sale', max_length=4, choices=[(b'sale', 'Vente'), (b'rent', 'Location')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='search',
            name='air_conditioning',
            field=ads.models.IndifferentBooleanField(verbose_name='Climatisation', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='alarm',
            field=ads.models.IndifferentBooleanField(verbose_name='Alarme', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='balcony',
            field=ads.models.IndifferentBooleanField(verbose_name='Balcon', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='bathroom',
            field=ads.models.IndifferentBooleanField(verbose_name='Salle de bain', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='cellar',
            field=ads.models.IndifferentBooleanField(verbose_name='Cave', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='digicode',
            field=ads.models.IndifferentBooleanField(verbose_name='Digicode', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='doorman',
            field=ads.models.IndifferentBooleanField(verbose_name='Gardien', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='duplex',
            field=ads.models.IndifferentBooleanField(verbose_name='Duplex', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='elevator',
            field=ads.models.IndifferentBooleanField(verbose_name='Ascenceur', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='fireplace',
            field=ads.models.IndifferentBooleanField(verbose_name='Chemin\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='ground_floor',
            field=ads.models.IndifferentBooleanField(default=None, verbose_name='Rez de chauss\xe9', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='habitation_types',
            field=models.ManyToManyField(to='ads.HabitationType', verbose_name="Types d'habitations"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='intercom',
            field=ads.models.IndifferentBooleanField(verbose_name='Interphone', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='kitchen',
            field=ads.models.IndifferentBooleanField(verbose_name='Cuisine \xe9quip\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='not_overlooked',
            field=ads.models.IndifferentBooleanField(verbose_name='Sans vis-\xe0-vis', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='parking',
            field=ads.models.IndifferentBooleanField(verbose_name='Parking', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='rooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nombre de pi\xe8ces minimum', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='separate_dining_room',
            field=ads.models.IndifferentBooleanField(verbose_name='Cuisine s\xe9par\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='separate_entrance',
            field=ads.models.IndifferentBooleanField(verbose_name='Entr\xe9e s\xe9par\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='separate_toilet',
            field=ads.models.IndifferentBooleanField(verbose_name='Toilettes s\xe9par\xe9s', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='shower',
            field=ads.models.IndifferentBooleanField(verbose_name="Salle d'eau (douche)", choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='swimming_pool',
            field=ads.models.IndifferentBooleanField(verbose_name='Piscine', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='terrace',
            field=ads.models.IndifferentBooleanField(verbose_name='Terrasse', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='top_floor',
            field=ads.models.IndifferentBooleanField(verbose_name='Dernier \xe9tage', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
    ]
