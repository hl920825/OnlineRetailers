from django.shortcuts import render

# Create your views here.

# 订单
def allorder(request):

    return render(request,'indent/allorder.html')