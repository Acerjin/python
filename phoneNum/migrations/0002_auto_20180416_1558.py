# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-16 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phoneNum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='dept',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='phoneNum.dwxx', verbose_name='部门'),
        ),
    ]