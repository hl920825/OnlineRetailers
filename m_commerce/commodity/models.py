from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel


# 商品分类表
class GoodsClass(BaseModel):
    class_name = models.CharField(max_length=50,verbose_name='分类名')
    class_intro = models.CharField(max_length=250,verbose_name='分类介绍',null=True)
    order = models.SmallIntegerField(default=0,verbose_name='排序')

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = 'goods_class'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

# 商品SPU表
class GoodsSpu(BaseModel):
    name = models.CharField(max_length=50,verbose_name='商品spu名称')
    desc = RichTextUploadingField(verbose_name='商品spu详情')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_spu'
        verbose_name = '商品Spu表'
        verbose_name_plural = verbose_name

# 商品单位表
class GoodsUnit(BaseModel):
    unitName = models.CharField(max_length=20,verbose_name='单位名称')

    def __str__(self):
        return self.unitName

    class Meta:
        db_table = 'goods_unit'
        verbose_name = '商品单位表'
        verbose_name_plural = verbose_name

# 商品相册表
class GoodsPhotos(BaseModel):
    image = models.ImageField(upload_to='goods/%Y%m',verbose_name='图片地址')
    goods_sku = models.ForeignKey(to='GoodsSku',verbose_name='商品sku_ID')

    def __str__(self):
        return "商品相册"

    class Meta:
        db_table = 'goods_photos'
        verbose_name = '商品相册表'
        verbose_name_plural = verbose_name


# 商品Sku表
class GoodsSku(BaseModel):
    goods_name = models.CharField(max_length=100,verbose_name='商品名')
    goods_intro = models.TextField(null=True,verbose_name='商品介绍')
    price = models.DecimalField(decimal_places=2,max_digits=10,verbose_name='商品价格')
    unit = models.ForeignKey(to='GoodsUnit',verbose_name='商品单位')
    num = models.PositiveIntegerField(verbose_name='库存')
    sellNum = models.PositiveIntegerField(verbose_name='销量')
    logo = models.ImageField(upload_to='goods/%Y%m',verbose_name='商品图片')
    is_putaway = models.BooleanField(default=False,verbose_name='是否上架')
    goods_cate = models.ForeignKey(to='GoodsClass',verbose_name='商品分类')
    goods_spu = models.ForeignKey(to='GoodsSpu',verbose_name='商品spu')

    def __str__(self):
        return self.goods_name

    class Meta:
        db_table = 'goods_sku'
        verbose_name = '商品sku表'
        verbose_name_plural = verbose_name

# 轮播
class Carousel(BaseModel):
    goods_name = models.CharField(max_length=150,verbose_name='轮播活动名称')
    goodsSku_id = models.ForeignKey(to='GoodsSku',max_length=50,verbose_name='商品id')
    image = models.ImageField(upload_to='banner/%Y%m/%d',verbose_name='图片地址')
    order = models.SmallIntegerField(verbose_name='排序',default=0)


    def __str__(self):
        return self.goods_name

    class Meta:
        db_table = 'Carousel'
        verbose_name = '轮播表'
        verbose_name_plural = verbose_name

# 首页活动
class Activity(BaseModel):
    title = models.CharField(verbose_name='活动名称',max_length=150)
    img_url = models.ImageField(verbose_name='活动图片地址',upload_to='activity/%Y%m/%d')
    activity_url = models.URLField(verbose_name='活动的url地址',max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '活动管理'
        verbose_name_plural = verbose_name

# 特色专区
class Activity_zone(BaseModel):
    title = models.CharField(verbose_name='活动专区名称',max_length=150)
    title_intro = models.CharField(verbose_name='活动专区简介',
                                   max_length=200,
                                   null=True,
                                   blank=True)
    order = models.SmallIntegerField(verbose_name='排序',
                                     default=0)
    is_putaway = models.BooleanField(verbose_name='是否上线',
                                     choices=((False,'下架'),(True,'上架'),),
                                     default=0)
    goods_sku = models.ManyToManyField(to='GoodsSku',verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '活动专区管理'
        verbose_name_plural = verbose_name




