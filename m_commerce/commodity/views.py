from django.shortcuts import render, redirect


# Create your views here.

# 城市
from commodity.models import GoodsClass,GoodsPhotos,GoodsSku,GoodsUnit,GoodsSpu




# 商品分类
def comcategory(request):
    if request.method == 'GET':
        # class_id = int(class_id)
        # 接收数据
        # class_id = int(class_id)
        # 查询商品分类未被删除的所有数据
        goods = GoodsClass.objects.filter(is_delete=False)

        # 根据传进来的class_id查询
        manyGoods = GoodsSku.objects.filter(is_delete=False)


        context = {
            'goods':goods,
            'manyGoods':manyGoods,
        }
        return render(request,'commodity/category.html',context=context)

def detail(request,id):
    # 当前商品信息
    goods = GoodsSku.objects.get(pk=id)
    context = {
        'goods':goods,
    }
    return render(request,'commodity/detail.html',context=context)

def city(request):
    return render(request,'commodity/city.html')

# 琳琅的店
def commodity_list(request):

    return render(request,'commodity/list.html')

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