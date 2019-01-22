from django.conf.urls import url

from commodity.views import commodity_list, comcategory, speedFood, recharge, hongbao, city, village, tidings

urlpatterns = [
    url('^commodity_list/$',commodity_list,name='琳琅的店'),
    url('^comcategory/$',comcategory,name='商品分类'),
    url('^speedFood/$',speedFood,name='飞速零食'),
    url('^recharge/$',recharge,name='充值'),
    url('^hongbao/$',hongbao,name='红包'),
    url('^city/$',city,name='城市定位'),
    url('^village/$',village,name='学校'),
    url('^tidings/$',tidings,name='消息'),
]