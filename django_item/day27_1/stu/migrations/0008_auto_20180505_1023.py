# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-05 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu', '0007_auto_20180505_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='s_status',
            field=models.CharField(choices=[('NONE', '正常'), ('NEXT_SCH', '留级'), ('DROP_SCH', '退学'), ('LEAVE_SCH', '休学')], default='NONE', max_length=30),
        ),
    ]
