# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0015_auto_20171117_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 17, 2, 58, 55, 321000)),
        ),
    ]