# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='hprovince',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='hpropre',
            field=models.CharField(default='', max_length=100, verbose_name='市'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='hcity',
            field=models.CharField(max_length=100, verbose_name='省'),
        ),
    ]
