from django.shortcuts import render, redirect


# Create your views here.

# 城市
def city(request):
    return render(request,'commodity/city.html')

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

# 学校
def village(request):
    return render(request,'commodity/village.html')

# 消息
def tidings(request):
    return render(request,'commodity/tidings.html')