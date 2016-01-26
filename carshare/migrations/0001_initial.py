# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 11:57
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, unique=True)),
                ('url', models.URLField(blank=True, max_length=120, null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Agenzia',
                'verbose_name_plural': 'Agenzie',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=20, unique=True)),
                ('design', models.CharField(blank=True, default=b'Unknown', max_length=40)),
                ('engine', models.CharField(blank=True, max_length=20, null=True)),
                ('kind', models.CharField(blank=True, max_length=20, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='carshare.Agency')),
            ],
            options={
                'ordering': ['plate'],
                'verbose_name': 'Veicolo',
                'verbose_name_plural': 'Veicoli',
            },
        ),
        migrations.CreateModel(
            name='VehicleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=120, null=True)),
                ('fuel', models.IntegerField(blank=True, null=True)),
                ('inside', models.IntegerField(blank=True, null=True)),
                ('outside', models.IntegerField(blank=True, null=True)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('webstamp', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='carshare.Vehicle')),
            ],
            options={
                'ordering': ['vehicle', 'stamp'],
                'verbose_name': 'Dati veicolo',
                'verbose_name_plural': 'Dati veicoli',
            },
        ),
        migrations.CreateModel(
            name='VehicleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=120, null=True)),
                ('fuel', models.IntegerField(blank=True, null=True)),
                ('inside', models.IntegerField(blank=True, null=True)),
                ('outside', models.IntegerField(blank=True, null=True)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('webstamp', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='carshare.Vehicle')),
            ],
            options={
                'ordering': ['vehicle', 'stamp'],
                'verbose_name': 'Stato veicolo',
                'verbose_name_plural': 'Stato veicoli',
            },
        ),
    ]
