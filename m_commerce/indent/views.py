from django.shortcuts import render
from django_redis import get_redis_connection
# Create your views here.

# 订单
def allorder(request):


    return render(request,'indent/allorder.html')

# 订单详情
def orderdetail(request):
    return render(request,'indent/orderdetail.html')