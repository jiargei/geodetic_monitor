# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-19 03:57
from __future__ import unicode_literals

import common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metering', '0003_auto_20160417_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='id',
            field=common.fields.UIDField(serialize=False),
        ),
    ]
