# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-08 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productfeatured'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatured',
            name='make_image_background',
            field=models.BooleanField(default=False),
        ),
    ]
