from django.contrib import admin

# Register your models here.
from commodity.models import GoodsClass,GoodsSku,GoodsSpu,GoodsUnit,GoodsPhotos

admin.site.register(GoodsClass)
admin.site.register(GoodsSpu)
admin.site.register(GoodsSku)
admin.site.register(GoodsUnit)
admin.site.register(GoodsPhotos)