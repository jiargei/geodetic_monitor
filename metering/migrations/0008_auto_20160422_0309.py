# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metering', '0007_auto_20160420_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='instrument_height',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_model',
            field=models.CharField(blank=True, choices=[(b'sensors.tachy.leica.leica_tachy_ts15.TS15', b'Leica Geosystems TS15'), (b'sensors.tachy.leica.leica_tachy_tm30.TM30', b'Leica Geosystems TM30'), (b'sensors.tachy.fake.fake_tachy.FakeTachy', b'FaKeBrAnD FaKeMoDeL'), (b'sensors.tachy.leica.leica_tachy_tps1100.TPS1100', b'Leica Geosystems TPS1100')], db_index=True, max_length=100, null=True),
        ),
    ]