# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-28 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0007_auto_20171225_1843.pyc'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodspot',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
