# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-29 17:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0014_auto_20171229_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodspotvote',
            name='foodSpot',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='foodspot.FoodSpot'),
        ),
        migrations.AlterField(
            model_name='foodspotvote',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='foodspotvote',
            name='value',
            field=models.SmallIntegerField(blank=True, choices=[(-1, 'Dislike'), (1, 'Like')]),
        ),
        migrations.AlterUniqueTogether(
            name='foodspotvote',
            unique_together=set([('owner', 'foodSpot')]),
        ),
    ]
