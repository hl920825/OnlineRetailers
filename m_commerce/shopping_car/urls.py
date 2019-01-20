from django.conf.urls import url

from shopping_car.views import shopcart_empty

urlpatterns = [
    url(r'^shopcart_empty/$',shopcart_empty,name='空购物车'),
]