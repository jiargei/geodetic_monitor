# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-08 20:34
from __future__ import unicode_literals

import bitfield.models
import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeWindow',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('frequency', models.DecimalField(decimal_places=1, default=10.0, max_digits=4)),
                ('day_of_week', bitfield.models.BitField(('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'), default=None)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
        ),
    ]
