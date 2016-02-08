# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 21:08
from __future__ import unicode_literals

import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationType',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('name', models.CharField(choices=[(b'dH', 'H\xf6hen\xe4nderung'), (b'dE', '\xc4nderung Rechtswert'), (b'dN', '\xc4nderung Hochwert'), (b'dl', 'L\xe4ngsverschiebung'), (b'dq', 'Querverschiebung'), (b'dS', 'Strecken\xe4nderung'), (b'dHz', '\xc4nderung Horizontalwinkel'), (b'dV', '\xc4nderung Vertikalwinkel')], max_length=20, unique=True)),
                ('unit', models.CharField(choices=[(b'm', b'Meter'), (b'dm', b'Dezimeter'), (b'cm', b'Zentimeter'), (b'mm', b'Millimeter'), (b'gon', b'Gon'), (b'mgon', b'Milligon')], max_length=10)),
                ('description', models.CharField(max_length=200)),
                ('scale', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('sensor_name', models.CharField(max_length=100)),
                ('sensor_serial', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', common.fields.UIDField(serialize=False)),
                ('easting', models.FloatField()),
                ('northing', models.FloatField()),
                ('height', models.FloatField()),
                ('name', models.CharField(max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
