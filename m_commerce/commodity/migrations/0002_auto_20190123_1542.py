# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 07:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsclass',
            options={'verbose_name': '商品分类', 'verbose_name_plural': '商品分类'},
        ),
        migrations.AlterModelOptions(
            name='goodsphotos',
            options={'verbose_name': '商品相册表', 'verbose_name_plural': '商品相册表'},
        ),
        migrations.AlterModelOptions(
            name='goodssku',
            options={'verbose_name': '商品sku表', 'verbose_name_plural': '商品sku表'},
        ),
        migrations.AlterModelOptions(
            name='goodsspu',
            options={'verbose_name': '商品Spu表', 'verbose_name_plural': '商品Spu表'},
        ),
        migrations.AlterModelOptions(
            name='goodsunit',
            options={'verbose_name': '商品单位表', 'verbose_name_plural': '商品单位表'},
        ),
    ]
