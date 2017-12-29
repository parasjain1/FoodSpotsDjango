# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-28 18:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodspot', '0012_auto_20171228_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSpotComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('foodSpot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='foodspot.FoodSpot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoodSpotVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(choices=[(-1, 'Dislike'), (1, 'Like')])),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('foodSpot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='foodspot.FoodSpot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
