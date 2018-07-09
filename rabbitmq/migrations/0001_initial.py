# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-09 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueueInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='\u961f\u5217\u540d\u79f0')),
                ('consumers', models.CharField(max_length=255, unique=True, verbose_name='\u6d88\u8d39\u8005\u96c6\u7fa4')),
                ('comment', models.CharField(max_length=255, null=True, verbose_name='\u63cf\u8ff0\u4fe1\u606f')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
