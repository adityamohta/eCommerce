# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-09 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
    ]
