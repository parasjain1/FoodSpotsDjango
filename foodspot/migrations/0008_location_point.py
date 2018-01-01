# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-27 19:09
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0007_auto_20171225_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
