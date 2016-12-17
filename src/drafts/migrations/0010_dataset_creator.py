# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drafts', '0009_remove_dataset_countries_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='creator',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
