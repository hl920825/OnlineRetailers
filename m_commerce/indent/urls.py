from django.conf.urls import url

from indent.views import allorder

urlpatterns = [
    url(r'^allorder/$',allorder,name='订单'),
]