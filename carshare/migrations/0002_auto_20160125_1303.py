# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'ordering': ['id', 'title'], 'verbose_name': 'Agenzia', 'verbose_name_plural': 'Agenzie'},
        ),
        migrations.AlterField(
            model_name='agency',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
