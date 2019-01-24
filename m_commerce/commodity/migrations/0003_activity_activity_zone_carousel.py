# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0002_auto_20190123_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('title', models.CharField(max_length=150, verbose_name='活动名称')),
                ('img_url', models.ImageField(upload_to='activity/%Y%m/%d', verbose_name='活动图片地址')),
                ('activity_url', models.URLField(verbose_name='活动的url地址')),
            ],
            options={
                'verbose_name': '活动管理',
                'verbose_name_plural': '活动管理',
            },
        ),
        migrations.CreateModel(
            name='Activity_zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('title', models.CharField(max_length=150, verbose_name='活动专区名称')),
                ('title_intro', models.CharField(blank=True, max_length=200, null=True, verbose_name='活动专区简介')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_putaway', models.BooleanField(choices=[(False, '下架'), (True, '上架')], default=0, verbose_name='是否上线')),
                ('goods_sku', models.ManyToManyField(to='commodity.GoodsSku', verbose_name='商品')),
            ],
            options={
                'verbose_name': '活动专区管理',
                'verbose_name_plural': '活动专区管理',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('goods_name', models.CharField(max_length=150, verbose_name='轮播活动名称')),
                ('image', models.ImageField(upload_to='banner/%Y%m/%d', verbose_name='图片地址')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('goodsSku_id', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='commodity.GoodsSku', verbose_name='商品id')),
            ],
            options={
                'verbose_name': '轮播表',
                'verbose_name_plural': '轮播表',
                'db_table': 'Carousel',
            },
        ),
    ]