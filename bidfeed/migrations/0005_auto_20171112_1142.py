# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 06:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0004_auto_20171108_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='current_bid',
        ),
        migrations.AddField(
            model_name='product',
            name='current_price',
            field=models.IntegerField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 12, 11, 42, 7, 283000)),
        ),
    ]