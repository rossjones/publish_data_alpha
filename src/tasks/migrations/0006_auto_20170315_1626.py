# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-15 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20170306_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='quantity',
            field=models.IntegerField(
                default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(
                choices=[
                    ('update',
                     'Update datasets'),
                    ('fix',
                     'Fix datasets'),
                    ('missing',
                     'Missing data')],
                max_length=20),
        ),
    ]
