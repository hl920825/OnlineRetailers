from django.conf.urls import url

from shopping_car.views import shopcart_empty, AddCartView, tureorder, order

urlpatterns = [
    url(r'^shopcart_empty/$',shopcart_empty,name='空购物车'),
    url(r'^addCart/$',AddCartView.as_view(),name='添加购物车'),
    url(r'^tureorder/$',tureorder,name='结算'),
    url(r'^order/$',order,name='提交订单'),
]