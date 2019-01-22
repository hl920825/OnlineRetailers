from django.shortcuts import render

# Create your views here.

# 订单
def allorder(request):

    return render(request,'indent/allorder.html')

# 订单详情
def orderdetail(request):
    return render(request,'indent/orderdetail.html')