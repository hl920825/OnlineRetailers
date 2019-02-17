from django.conf.urls import url

from indent.views import allorder, orderdetail

urlpatterns = [
    url(r'^allorder/$',allorder,name='订单'),
    url(r'^orderdetail/(?P<id>\d+)/$',orderdetail,name='订单详情'),
]