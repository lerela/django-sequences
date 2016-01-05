# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='name')),
                ('last', models.PositiveIntegerField(verbose_name='last value')),
            ],
            options={
                'verbose_name': 'sequence',
                'verbose_name_plural': 'sequences',
            },
        ),
    ]
