# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-14 17:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='listing_type',
            new_name='listing',
        ),
    ]
