# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 13:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0003_auto_20171108_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default=b'general', max_length=100),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_value',
            field=models.IntegerField(max_length=250),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 8, 18, 33, 48, 56000)),
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_increase',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_price',
            field=models.IntegerField(default=0),
        ),
    ]
