from django.shortcuts import render
from django_redis import get_redis_connection
# Create your views here.

# 订单
from indent.models import Order


def allorder(request):

    if request.method == "GET":
        # 获取所有订单模型中的订单
        orders = Order.objects.filter(is_delete=False)
        context = {
            "orders":orders,
        }
        return render(request,'indent/allorder.html',context=context)

# 订单详情
def orderdetail(request,id):
    if request.method == "GET":
        order = Order.objects.get(pk=id)
        context = {
            "order":order,
        }
        return render(request,'indent/orderdetail.html',context=context)