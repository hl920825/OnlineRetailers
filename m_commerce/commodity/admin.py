from django.contrib import admin

# Register your models here.
from commodity.models import GoodsClass,GoodsSku,GoodsSpu,GoodsUnit,GoodsPhotos,Carousel,Activity,Activity_zone

# admin.site.register(GoodsClass)
# admin.site.register(GoodsSku)
admin.site.register(GoodsSpu)
admin.site.register(GoodsUnit)
admin.site.register(GoodsPhotos)
admin.site.register(Carousel)
admin.site.register(Activity)
# admin.site.register(Activity_zone)

@admin.register(GoodsClass)
class GoodsClassAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id','class_name','class_intro','change_time','order']
    list_display_links = ['id','class_name','class_intro']

class GoodsPhotosInline(admin.TabularInline):
    model = GoodsPhotos
    extra = 2

@admin.register(GoodsSku)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ["id", 'goods_name', 'price', 'unit', 'num', 'sellNum', 'is_putaway', 'goods_cate']
    list_display_links = ["id", 'goods_name', 'price']
    list_editable = ['is_putaway']
    search_fields = ['goods_name', 'price', 'sellNum']
    inlines = [
        GoodsPhotosInline,
    ]

@admin.register(Activity_zone)
class ActivityZoneAdmin(admin.ModelAdmin):
    pass