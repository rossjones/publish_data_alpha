# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 14:05
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0009_auto_20170117_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='title', unique=True),
        ),
    ]