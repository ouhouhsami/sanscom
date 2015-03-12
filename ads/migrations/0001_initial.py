# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'slug_format', verbose_name='slug', editable=False, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('address', models.CharField(max_length=255, verbose_name='Adresse')),
                ('price', models.PositiveIntegerField(verbose_name='Prix')),
                ('surface', models.IntegerField(verbose_name='Surface habitable')),
                ('surface_carrez', models.IntegerField(null=True, verbose_name='Surface Loi Carrez', blank=True)),
                ('rooms', models.PositiveIntegerField(verbose_name='Nombre de pi\xe8ces')),
                ('bedrooms', models.PositiveIntegerField(verbose_name='Nombre de chambres')),
                ('energy_consumption', models.CharField(blank=True, max_length=1, null=True, verbose_name='Consommation \xe9nerg\xe9tique (kWhEP/m\xb2.an)', choices=[(b'A', 'A - \u2264 50'), (b'B', 'B - 51 \xe0 90'), (b'C', 'C - 91 \xe0 150'), (b'D', 'D - 151 \xe0 230'), (b'E', 'E - 231 \xe0 330'), (b'F', 'F - 331 \xe0 450'), (b'G', 'G - > 450')])),
                ('ad_valorem_tax', models.IntegerField(help_text='Montant annuel, sans espace, sans virgule', null=True, verbose_name='Taxe fonci\xe8re', blank=True)),
                ('housing_tax', models.IntegerField(help_text='Montant annuel, sans espace, sans virgule', null=True, verbose_name="Taxe d'habitation", blank=True)),
                ('maintenance_charges', models.IntegerField(help_text='Montant mensuel, sans espace, sans virgule', null=True, verbose_name='Charges', blank=True)),
                ('emission_of_greenhouse_gases', models.CharField(blank=True, max_length=1, null=True, verbose_name='\xc9missions de gaz \xe0 effet de serre (kgeqCO2/m\xb2.an)', choices=[(b'A', 'A - \u2264 5'), (b'B', 'B - 6 \xe0 10'), (b'C', 'C - 11 \xe0 20'), (b'D', 'D - 21 \xe0 35'), (b'E', 'E - 36 \xe0 55'), (b'F', 'F - 56 \xe0 80'), (b'G', 'G - > 80')])),
                ('ground_surface', models.IntegerField(null=True, verbose_name='Surface du terrain', blank=True)),
                ('floor', models.PositiveIntegerField(null=True, verbose_name='Etage', blank=True)),
                ('ground_floor', models.BooleanField(verbose_name='Rez de chauss\xe9')),
                ('top_floor', models.BooleanField(verbose_name='Dernier \xe9tage')),
                ('not_overlooked', models.BooleanField(verbose_name='Sans vis-\xe0-vis')),
                ('elevator', models.BooleanField(verbose_name='Ascenceur')),
                ('intercom', models.BooleanField(verbose_name='Interphone')),
                ('digicode', models.BooleanField(verbose_name='Digicode')),
                ('doorman', models.BooleanField(verbose_name='Gardien')),
                ('heating', models.CharField(blank=True, max_length=2, null=True, verbose_name='Chauffage', choices=[(b'1', 'individuel gaz'), (b'2', 'individuel \xe9lectrique'), (b'3', 'collectif gaz'), (b'4', 'collectif fuel'), (b'5', 'collectif r\xe9seau de chaleur'), (b'13', 'autres')])),
                ('kitchen', models.BooleanField(verbose_name='Cuisine \xe9quip\xe9e')),
                ('duplex', models.BooleanField(verbose_name='Duplex')),
                ('swimming_pool', models.BooleanField(verbose_name='Piscine')),
                ('alarm', models.BooleanField(verbose_name='Alarme')),
                ('air_conditioning', models.BooleanField(verbose_name='Climatisation')),
                ('fireplace', models.CharField(blank=True, max_length=2, null=True, verbose_name='Chemin\xe9e', choices=[(b'1', 'Foyer ouvert'), (b'2', 'Insert')])),
                ('terrace', models.IntegerField(null=True, verbose_name='Terrasse', blank=True)),
                ('balcony', models.IntegerField(null=True, verbose_name='Balcon', blank=True)),
                ('separate_dining_room', models.BooleanField(verbose_name='Cuisine s\xe9par\xe9e')),
                ('separate_toilet', models.IntegerField(null=True, verbose_name='Toilettes s\xe9par\xe9s', blank=True)),
                ('bathroom', models.IntegerField(null=True, verbose_name='Salle de bain', blank=True)),
                ('shower', models.IntegerField(null=True, verbose_name="Salle d'eau (douche)", blank=True)),
                ('separate_entrance', models.BooleanField(verbose_name='Entr\xe9e s\xe9par\xe9e')),
                ('cellar', models.BooleanField(verbose_name='Cave')),
                ('parking', models.CharField(blank=True, max_length=2, null=True, verbose_name='Parking', choices=[(b'1', 'Place de parking'), (b'2', 'Box ferm\xe9')])),
                ('orientation', models.CharField(max_length=255, null=True, verbose_name='Orientation', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'pictures/%Y/%m/%d', verbose_name=b'Photo')),
                ('title', models.CharField(max_length=255, null=True, verbose_name=b'Titre', blank=True)),
                ('ad', models.ForeignKey(to='ads.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdSearchRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('ad_notified', models.DateTimeField(null=True, blank=True)),
                ('search_notified', models.DateTimeField(null=True, blank=True)),
                ('ad_contacted', models.DateTimeField(null=True, blank=True)),
                ('search_contacted', models.DateTimeField(null=True, blank=True)),
                ('valid', models.BooleanField()),
                ('ad', models.ForeignKey(to='ads.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HabitationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'slug_format', verbose_name='slug', editable=False, blank=True)),
                ('location', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('price_max', models.PositiveIntegerField(verbose_name='Prix max')),
                ('surface_min', models.PositiveIntegerField(verbose_name='Surface min')),
                ('habitation_types', models.ManyToManyField(to='ads.HabitationType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='adsearchrelation',
            name='search',
            field=models.ForeignKey(to='ads.Search'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='adsearchrelation',
            unique_together=set([('ad', 'search')]),
        ),
        migrations.AddField(
            model_name='ad',
            name='habitation_type',
            field=models.ForeignKey(verbose_name=b'Type de bien', to='ads.HabitationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
