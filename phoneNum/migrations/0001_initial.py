# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-16 07:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cljl',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('xm', models.CharField(max_length=10, verbose_name='姓名')),
                ('ybh', models.IntegerField(verbose_name='医保号')),
                ('bglx', models.CharField(blank=True, max_length=10, null=True, verbose_name='变更类型')),
                ('clz', models.CharField(max_length=10, verbose_name='处理者')),
                ('clsj', models.DateTimeField(auto_now_add=True, verbose_name='处理时间')),
            ],
            options={
                'verbose_name': '处理记录表',
                'verbose_name_plural': '处理记录表',
            },
        ),
        migrations.CreateModel(
            name='dclxxb',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('xm', models.CharField(max_length=10, verbose_name='姓名')),
                ('ybh', models.IntegerField(verbose_name='医保号')),
                ('yhm', models.CharField(blank=True, max_length=11, null=True, verbose_name='原电话号码')),
                ('xhm', models.CharField(blank=True, max_length=11, null=True, verbose_name='新号码')),
                ('fbz', models.CharField(max_length=10, verbose_name='发布者')),
                ('fbsj', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('bz', models.CharField(blank=True, max_length=10, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '待处理信息表',
                'verbose_name_plural': '待处理信息表',
            },
        ),
        migrations.CreateModel(
            name='dwxx',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dwbm', models.IntegerField(verbose_name='单位编码')),
                ('dwmc', models.CharField(max_length=50, verbose_name='单位名称')),
                ('dwcwsx', models.CharField(max_length=10, verbose_name='单位财务属性')),
            ],
            options={
                'verbose_name': '单位信息',
                'verbose_name_plural': '单位信息',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.CharField(blank=True, max_length=200, null=True, verbose_name='部门')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='dclxxb',
            name='dwmc',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='phoneNum.dwxx', verbose_name='单位名称'),
        ),
        migrations.AddField(
            model_name='cljl',
            name='dwbm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phoneNum.dwxx', verbose_name='单位编码'),
        ),
    ]
