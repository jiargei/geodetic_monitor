# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 17:24
from __future__ import unicode_literals

import bitfield.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timewindow',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='content_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='day_of_week',
            field=bitfield.models.BitField(('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'), default=None),
        ),
        migrations.AddField(
            model_name='task',
            name='end_time',
            field=models.TimeField(default="0:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='frequency',
            field=models.DecimalField(decimal_places=1, default=10.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='task',
            name='object_id',
            field=models.CharField(db_index=True, default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='start_time',
            field=models.TimeField(default="0:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='task',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='time_windows', to='tasks.Task'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TimeWindow',
        ),
    ]
