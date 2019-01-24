from django.shortcuts import render, redirect


# Create your views here.

# 城市
from commodity.models import GoodsClass,GoodsPhotos,GoodsSku,GoodsUnit,GoodsSpu




# 商品分类
def comcategory(request,class_id,order):
    if request.method == 'GET':
        # class_id = int(class_id)
        # 接收数据
        # class_id = int(class_id)
        # 查询商品分类未被删除的所有数据
        goods = GoodsClass.objects.filter(is_delete=False).order_by('-order')
        """
        添加一个参数order
        0:综合
        1:销量
        2:价格升
        3:价格降
        4:添加时间降
        """
        # 取出第一个分类
        if class_id == '':
            category =  goods.first()
            class_id = category.pk
        else:
            # 根据分类id查询对应的分类
            class_id = int(class_id)
            category = GoodsClass.objects.get(pk=class_id)

        # 根据传进来的class_id查询
        # 查询对应类下的所有商品
        manyGoods = GoodsSku.objects.filter(is_delete=False,goods_cate=category)

        if order == '':
            order = 0
        order = int(order)

        # if order == 0:
        #     manyGoods = manyGoods.order_by('pk')
        # elif order == 1:
        #     manyGoods = manyGoods.order_by('-sellNum')
        # elif order == 2:
        #     manyGoods = manyGoods.order_by('price')
        # elif order == 3:
        #     manyGoods = manyGoods.order_by('-price')
        # elif order == 4:
        #     manyGoods = manyGoods.order_by('-add_time')

        # 排序规则列表
        order_rule = ['pk','-sellNum','price','-price','-add_time']
        manyGoods = manyGoods.order_by(order_rule[order])


        context = {
            'goods':goods,
            'manyGoods':manyGoods,
            'class_id':class_id,
            'order':order,
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