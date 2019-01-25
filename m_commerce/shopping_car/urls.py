from django.conf.urls import url

from shopping_car.views import shopcart_empty, AddCartView

urlpatterns = [
    url(r'^shopcart_empty/$',shopcart_empty,name='空购物车'),
    url(r'^addCart/$',AddCartView.as_view(),name='添加购物车'),
]