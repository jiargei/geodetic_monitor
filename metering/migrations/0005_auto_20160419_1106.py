# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 09:06
from __future__ import unicode_literals

import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('metering', '0004_auto_20160419_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('p1_easting', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('p1_northing', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('p2_easting', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('p2_northing', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Project')),
            ],
        ),
        migrations.AddField(
            model_name='target',
            name='point_type',
            field=models.CharField(choices=[(b'd', b'Deformationspunkt'), (b'f', b'Festpunkt')], default='d', max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='targets',
            field=models.ManyToManyField(related_name='profiles', to='metering.Target'),
        ),
    ]