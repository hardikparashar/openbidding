# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 17:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0012_auto_20171116_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='csvf',
            field=models.FileField(blank=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 16, 23, 6, 49, 760000)),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default=b'name', max_length=400),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_price',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
