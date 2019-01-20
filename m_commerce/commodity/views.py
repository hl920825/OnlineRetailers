from django.shortcuts import render

# Create your views here.

# 琳琅的店
def commodity_list(request):

    return render(request,'commodity/list.html')

# 商品分类
def comcategory(request):

    return render(request,'commodity/category.html')

# 飞速零食
def speedFood(request):
    return render(request,'commodity/speed.html')

# 充值
def recharge(request):
    return render(request,'commodity/recharge.html')

# 红包
def hongbao(request):
    return render(request,'users/yhq.html')