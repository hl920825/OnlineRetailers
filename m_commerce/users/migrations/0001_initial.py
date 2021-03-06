# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-20 02:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNum', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11, '手机号应为11位')])),
                ('nickName', models.CharField(max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(2, '昵称至少为2个字符')])),
                ('password', models.CharField(max_length=32)),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3)),
                ('school', models.CharField(max_length=200, null=True)),
                ('home_address', models.CharField(max_length=200, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('change_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
