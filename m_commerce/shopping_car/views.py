from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from commodity.models import GoodsSku
from db.base_view import VerifyLoginView
from indent.models import UserAddress, Transport
from shopping_car.cart_helper import json_msg, get_cart_count
from django_redis import get_redis_connection

# 购物车
from shopping_car.helper import get_cart_key
from users.helper import check_login


@check_login
def shopcart_empty(request):
    # 连接redis
    r = get_redis_connection()
    # 从redis中将保存的商品及数量全部取出来
    i = request.session.get("ID")
    cart_key = "cart_%s"%i
    cart = r.hgetall(cart_key)
    # print(cart)  # 字典
    # 使用列表存所有的商品
    goodsList = []
    # 总价格
    # total_price = 0
    # 遍历字典
    for sku_id,count in cart.items():
        sku_id = int(sku_id)
        count = int(count)
        # 获取商品信息
        goods = GoodsSku.objects.get(pk=sku_id,is_delete=False)
        goods.count = count
        goodsList.append(goods)
        # total_price += goods.price * count

    context = {
        'goodsList':goodsList,
        # 'total_price':total_price,
    }
    return render(request,'shopping_car/shopcart.html',context=context)

# 添加购物车
class AddCartView(VerifyLoginView):
    # 操作购物车,添加购物车数据
    def post(self,request):
        # 接收三个参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 判断是整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1,"参数错误!"))

        # 在数据库中要存在有商品
        try:
            goods_sku = GoodsSku.objects.get(pk=sku_id)
        except GoodsSku.DoesNotExist:
            return JsonResponse(json_msg(2,"商品不存在"))

        # 判断库存
        # 创建redis连接
        r = get_redis_connection()
        # 处理购物车的key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取已经存在的  加  需要添加的   再与库存进行比较
        exist_count = r.hget(cart_key,sku_id)  # 得到的二进制的数据
        if exist_count is None:
            exist_count = 0
        else:
            exist_count = int(exist_count)

        if goods_sku.num < exist_count + count:
            return JsonResponse(json_msg(3,"库存不足!"))

        # 将商品添加到购物车
        rs = r.hincrby(cart_key,sku_id,count)

        # 商品数量为0时删除该商品
        if rs <= 0:
            # 删除field
            r.hdel(cart_key,sku_id)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 合成响应
        return JsonResponse(json_msg(0,"添加购物车成功",data=cart_count))

# 结算/提交订单
def tureorder(request):
    if request.method == "GET":
        user_id = request.session.get("ID")
        # 收货地址
        address = UserAddress.objects.filter(user=user_id).order_by("-isDefault").first()

        # 处理商品信息
        sku_ids = request.GET.getlist("sku_ids")
        goods_skus = []
        goods_totalPrice = 0

        # 创建redis连接
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)
        # 遍历
        for sku_id in sku_ids:
            try:
                goods_sku = GoodsSku.objects.get(pk=sku_id)
            except GoodsSku.DoesNotExist:
                # 不存在的话就返回购物车列表
                return redirect("shopping_car:空购物车")

            # 获取对应商品的数量
            try:
                count = r.hget(cart_key,sku_id)
                count = int(count)
            except:
                return redirect("shopping_car:空购物车")

            # 保存到商品对象上
            goods_sku.count = count
            goods_skus.append(goods_sku)

            # 统计商品总计
            goods_totalPrice += goods_sku.price * count
        # 获取运输方式
        transports = Transport.objects.filter(is_delete=False).order_by('price')

        # 渲染数据
        context = {
            'address':address,
            'goods_skus':goods_skus,
            'goods_total_price':goods_totalPrice,
            'transports':transports,
        }
        return render(request,'shopping_car/tureorder.html',context=context)

# 提交订单
def order(request):
    return render(request,'shopping_car/order.html')



