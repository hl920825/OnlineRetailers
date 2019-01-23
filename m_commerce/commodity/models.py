from django.db import models

# Create your models here.
from db.base_model import BaseModel


# 商品分类表
class GoodsClass(BaseModel):
    class_name = models.CharField(max_length=50,verbose_name='分类名')
    class_intro = models.CharField(max_length=250,verbose_name='分类介绍',null=True)

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = 'goods_class'
        verbose_name = '商品分类'

# 商品SPU表
class GoodsSpu(BaseModel):
    name = models.CharField(max_length=50,verbose_name='商品spu名称')
    desc = models.TextField(null=True,verbose_name='商品spu描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_spu'
        verbose_name = '商品Spu表'

# 商品单位表
class GoodsUnit(BaseModel):
    unitName = models.CharField(max_length=20,verbose_name='单位名称')

    def __str__(self):
        return self.unitName

    class Meta:
        db_table = 'goods_unit'
        verbose_name = '商品单位表'

# 商品相册表
class GoodsPhotos(BaseModel):
    image = models.ImageField(upload_to='goods/%Y%m',verbose_name='图片地址')
    goods_sku = models.ForeignKey(to='GoodsSku',verbose_name='商品sku_ID')

    def __str__(self):
        return self.goods_sku

    class Meta:
        db_table = 'goods_photos'
        verbose_name = '商品相册表'


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