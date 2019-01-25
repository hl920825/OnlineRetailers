from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from commodity.models import GoodsSku
from db.base_view import VerifyLoginView
from shopping_car.cart_helper import json_msg, get_cart_count
from django_redis import get_redis_connection


def shopcart_empty(request):

    return render(request,'shopping_car/shopcart.html')

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
        r.hincrby(cart_key,sku_id,count)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 合成响应
        return JsonResponse(json_msg(0,"添加购物车成功",data=cart_count))






