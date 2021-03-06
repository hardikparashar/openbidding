# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bidfeed', '0002_auto_20171107_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='days',
            field=models.IntegerField(default=b'2', help_text=b'enter in days'),
        ),
        migrations.AddField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='rem_days',
            field=models.IntegerField(default=b'2', help_text=b'enter in days'),
        ),
    ]
