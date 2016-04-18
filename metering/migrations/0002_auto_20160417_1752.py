# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-17 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('metering', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='station',
            options={'get_latest_by': 'from_date', 'ordering': ['-from_date']},
        ),
        migrations.AddField(
            model_name='station',
            name='box',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='box', to='accounts.Box'),
        ),
        migrations.AddField(
            model_name='station',
            name='port',
            field=models.FileField(blank=True, null=True, upload_to='/dev/'),
        ),
        migrations.AlterField(
            model_name='station',
            name='from_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='station',
            name='to_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]