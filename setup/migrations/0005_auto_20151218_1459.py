# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 13:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_auto_20151216_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='bis',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 18, 14, 59, 5, 962000)),
        ),
        migrations.AlterField(
            model_name='station',
            name='von',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 18, 14, 59, 5, 961000)),
        ),
    ]
