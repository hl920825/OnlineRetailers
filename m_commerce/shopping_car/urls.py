from django.conf.urls import url

from shopping_car.views import shopcart_empty, AddCartView, ShowOrder,TureOrder,Pay

urlpatterns = [
    url(r'^shopcart_empty/$',shopcart_empty,name='空购物车'),
    url(r'^addCart/$',AddCartView.as_view(),name='添加购物车'),
    # url(r'^tureorder/$',tureorder,name='结算'),
    url(r'^tureorder/$',TureOrder.as_view(),name='结算'),
    url(r'^order/$',ShowOrder.as_view(),name='确认支付'),
    url(r'^pay/$',Pay.as_view(),name='支付结果'),
]