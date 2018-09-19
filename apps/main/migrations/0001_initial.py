# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-19 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('permissionLevel', models.CharField(choices=[('U', 'USER'), ('G', 'AGENT'), ('A', 'ADMINISTRATOR')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
