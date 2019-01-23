# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('class_name', models.CharField(max_length=50, verbose_name='分类名')),
                ('class_intro', models.CharField(max_length=250, null=True, verbose_name='分类介绍')),
            ],
            options={
                'verbose_name': '商品分类',
                'db_table': 'goods_class',
            },
        ),
        migrations.CreateModel(
            name='GoodsPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('image', models.ImageField(upload_to='goods/%Y%m', verbose_name='图片地址')),
            ],
            options={
                'verbose_name': '商品相册表',
                'db_table': 'goods_photos',
            },
        ),
        migrations.CreateModel(
            name='GoodsSku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('goods_name', models.CharField(max_length=100, verbose_name='商品名')),
                ('goods_intro', models.TextField(null=True, verbose_name='商品介绍')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('num', models.PositiveIntegerField(verbose_name='库存')),
                ('sellNum', models.PositiveIntegerField(verbose_name='销量')),
                ('logo', models.ImageField(upload_to='goods/%Y%m', verbose_name='商品图片')),
                ('is_putaway', models.BooleanField(default=False, verbose_name='是否上架')),
                ('goods_cate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.GoodsClass', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品sku表',
                'db_table': 'goods_sku',
            },
        ),
        migrations.CreateModel(
            name='GoodsSpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=50, verbose_name='商品spu名称')),
                ('desc', models.TextField(null=True, verbose_name='商品spu描述')),
            ],
            options={
                'verbose_name': '商品Spu表',
                'db_table': 'goods_spu',
            },
        ),
        migrations.CreateModel(
            name='GoodsUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('change_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('unitName', models.CharField(max_length=20, verbose_name='单位名称')),
            ],
            options={
                'verbose_name': '商品单位表',
                'db_table': 'goods_unit',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods_spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.GoodsSpu', verbose_name='商品spu'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.GoodsUnit', verbose_name='商品单位'),
        ),
        migrations.AddField(
            model_name='goodsphotos',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.GoodsSku', verbose_name='商品sku_ID'),
        ),
    ]
