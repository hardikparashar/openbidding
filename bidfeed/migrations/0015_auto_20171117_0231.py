# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0014_auto_20171116_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 11, 17, 2, 31, 40, 675000)),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.FileField(blank=True, upload_to=b''),
        ),
    ]