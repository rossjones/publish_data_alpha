# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-27 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_auto_20170127_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='locations',
        ),
        migrations.AddField(
            model_name='dataset',
            name='location1',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='dataset',
            name='location2',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='dataset',
            name='location3',
            field=models.TextField(blank=True, default=''),
        ),
    ]