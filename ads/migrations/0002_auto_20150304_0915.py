# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_habitation_types(apps, schema_editor):
    HabitationType = apps.get_model("ads", "HabitationType")
    db_alias = schema_editor.connection.alias
    HabitationType.objects.using(db_alias).bulk_create([
        HabitationType(label="Appartement"),
        HabitationType(label="Maison")
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_habitation_types),
    ]
