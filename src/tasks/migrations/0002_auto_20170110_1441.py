# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-10 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('update', 'Update datasets'), ('fix', 'Fix datasets')], max_length=20),
        ),
    ]
