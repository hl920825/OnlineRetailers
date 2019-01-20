from django.conf.urls import url

from commodity.views import commodity_list, comcategory

urlpatterns = [
    url('^commodity_list/$',commodity_list,name='商品列表'),
    url('^comcategory/$',comcategory,name='商品分类'),
]