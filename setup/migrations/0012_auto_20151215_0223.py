# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 01:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0011_auto_20151215_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='recent_sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.Sensor'),
        ),
        migrations.AlterField(
            model_name='station',
            name='bis',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 15, 2, 23, 43, 309396)),
        ),
        migrations.AlterField(
            model_name='station',
            name='von',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 15, 2, 23, 43, 309356)),
        ),
    ]