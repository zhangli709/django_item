# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-27 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='u_ticket',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
