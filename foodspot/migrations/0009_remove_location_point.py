# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-27 19:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0008_location_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='point',
        ),
    ]