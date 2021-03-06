# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-28 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0011_user_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodspot',
            name='preApproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='credits',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
