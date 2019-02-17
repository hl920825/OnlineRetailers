import os
import random
from datetime import datetime
from time import sleep

from alipay import AliPay
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from commodity.models import GoodsSku
from db.base_view import VerifyLoginView
from indent.models import UserAddress, Transport, Order, OrderGoods, Payment
from shopping_car.cart_helper import json_msg, get_cart_count
from django_redis import get_redis_connection


from shopping_car.helper import get_cart_key
from users.helper import check_login
from users.models import Users

# 购物车
@check_login
def shopcart_empty(request):
    # 连接redis
    r = get_redis_connection()
    # 从redis中将保存的商品及数量全部取出来
    i = request.session.get("ID")
    cart_key = "cart_%s" % i
    cart = r.hgetall(cart_key)
    # print(cart)  # 字典
    # 使用列表存所有的商品
    goodsList = []
    # 总价格
    # total_price = 0
    # 遍历字典
    for sku_id, count in cart.items():
        sku_id = int(sku_id)
        count = int(count)
        # 获取商品信息
        goods = GoodsSku.objects.get(pk=sku_id, is_delete=False)
        goods.count = count
        goodsList.append(goods)
        # total_price += goods.price * count

    context = {
        'goodsList': goodsList,
        # 'total_price':total_price,
    }
    return render(request, 'shopping_car/shopcart.html', context=context)


# 添加购物车
class AddCartView(VerifyLoginView):
    # 操作购物车,添加购物车数据
    def post(self, request):
        # 接收三个参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 判断是整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误!"))

        # 在数据库中要存在有商品
        try:
            goods_sku = GoodsSku.objects.get(pk=sku_id)
        except GoodsSku.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在"))

        # 判断库存
        # 创建redis连接
        r = get_redis_connection()
        # 处理购物车的key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取已经存在的  加  需要添加的   再与库存进行比较
        exist_count = r.hget(cart_key, sku_id)  # 得到的二进制的数据
        if exist_count is None:
            exist_count = 0
        else:
            exist_count = int(exist_count)

        if goods_sku.num < exist_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 将商品添加到购物车
        rs = r.hincrby(cart_key, sku_id, count)

        # 商品数量为0时删除该商品
        if rs <= 0:
            # 删除field
            r.hdel(cart_key, sku_id)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))


# 结算/提交订单
class TureOrder(View):
    def get(self, request):
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
                count = r.hget(cart_key, sku_id)
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
            'address': address,
            'goods_skus': goods_skus,
            'goods_total_price': goods_totalPrice,
            'transports': transports,
        }
        return render(request, 'shopping_car/tureorder.html', context=context)

    def post(self, request):
        # 保存订单数据
        # 接收参数
        transport_id = request.POST.get('transport')
        sku_ids = request.POST.getlist('sku_ids')
        address_id = request.POST.get('address')
        # print(sku_ids)
        # 接收用户id
        user_id = request.session.get("ID")
        user = Users.objects.get(pk=user_id)
        # print(user)
        # 验证数据合法性
        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(2, "参数错误"))
        # 验证收货地址和运输方式存在
        try:
            address = UserAddress.objects.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在!"))
        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在!"))
        # 操作数据
        sid = transaction.savepoint()
        # 操作订单基本信息表
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.brief)
        try:
            order = Order.objects.create(
                uer=user,
                order_sn=order_sn,
                transport_price=transport.price,
                transport=transport.name,
                username=address.username,
                phone=address.phone,
                address=address_info
            )
        except:
            return JsonResponse(json_msg(8,"创建订单基本数据失败"))
        # 操作订单商品表
        # 操作redis
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)
        # 准备一个变量保存商品总金额
        goods_total_price = 0
        for sku_id in sku_ids:
            # 获取商品对象
            try:
                goods_sku = GoodsSku.objects.select_for_update().get(pk=sku_id, is_delete=False)
            except GoodsSku.DoesNotExist:
                # 回滚数据
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(5, "商品不存在!"))
            # 获取购物车中商品的数量
            # redis基于内存的存储,有可能数据会丢失
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(6, "购物车中数量不存在!"))
            # 判断库存是否足够
            if goods_sku.num < count:
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(7, "库存不足!"))
            # 保存订单商品表
            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count
            )
            # 添加商品总金额
            goods_total_price += goods_sku.price * count

            # 扣除库存,销量增加
            goods_sku.num -= count
            goods_sku.sellNum += count
            goods_sku.save()

        # 操作订单基本信息表
        # 订单总金额
        try:
            order_price = goods_total_price + transport.price
            order.goods_totalPrice = goods_total_price
            order.order_price = order_price
            order.save()
        except:
            # 回滚
            transaction.savepoint_rollback(sid)
            return JsonResponse(json_msg(9,"更新订单失败"))

        # 清空redis中的购物车数据
        r.hdel(cart_key, *sku_ids)

        # 下单成功,提交事务
        transaction.savepoint_commit(sid)

        # 合成响应
        return JsonResponse(json_msg(0, "创建订单成功!", data=order_sn))


# 提交订单
class ShowOrder(VerifyLoginView):
    def get(self,request):
        # 接收参数
        order_sn = request.GET.get("order_sn")
        user_id = request.session.get("ID")
        # 操作数据
        # 获取订单信息
        order = Order.objects.get(order_sn=order_sn,uer_id=user_id)

        # 获取支付方式
        payments = Payment.objects.filter(is_delete=False).order_by("id")

        context = {
            "order":order,
            "payments":payments,
        }

        return render(request,"shopping_car/order.html",context=context)
    def post(self,request):
        # 接收参数
        payment = request.POST.get("payment")
        order_sn = request.POST.get("order_sn")
        user_id = request.session.get("ID")
        # 判断参数合法性
        try:
            payment = int(payment)
        except:
            return JsonResponse(json_msg(1,"参数错误"))

        # 支付方式存在
        try:
            payment = Payment.objects.get(pk=payment)
        except Payment.DoesNotExist:
            return JsonResponse(json_msg(2,"支付方式不存在"))

        # 判断该订单是否是自己的,并且是一个未支付的订单
        try:
            order = Order.objects.get(uer_id=user_id,order_sn=order_sn,order_status=0)
        except Order.DoesNotExist:
            return JsonResponse(json_msg(3,"订单不满足要求"))

        # 判断用户是否需要使用支付宝支付
        if payment.name == "支付宝":
            # 构造支付请求
            app_private_key_string = open(os.path.join(settings.BASE_DIR,"alipay/app_private_key_string.txt")).read()
            alipay_public_key_string = open(os.path.join(settings.BASE_DIR,"alipay/alipay_public_key_string.txt")).read()

            # 初始化对象
            alipay = AliPay(
                appid="2016092400582468",
                app_notify_url=None, # 默认回调url
                app_private_key_string=app_private_key_string,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",   # RSA 或者 RSA2
                debug=True # 默认False
            )

            # 构造请求地址
            order_string = alipay.api_alipay_trade_wap_pay(
                out_trade_no=order.order_sn,  # 订单编号
                total_amount=str(order.order_price),  # 订单金额
                subject="超市订单支付",  # 订单描述
                return_url="http://127.0.0.1:8002/shopping_car/pay/",  # 同步通知地址
                notify_url=None  # 异步通知地址
            )
            # 拼接地址
            url = "https://openapi.alipaydev.com/gateway.do?" + order_string

            # 通过json返回请求地址
            return JsonResponse(json_msg(0, "创建支付地址成功", data=url))
        else:
            return JsonResponse(json_msg(4, "该支付方式暂不支支持"))

# 展示支付结果
class Pay(VerifyLoginView):
    def get(self,request):
        # 查询订单是否交易成功
        # 构造支付请求
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/app_private_key_string.txt")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key_string.txt')).read()
        # 初始化对象
        alipay = AliPay(
            appid="2016092400582468",
            app_notify_url=None,    # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=True
        )
        # 获取订单编号
        order_sn = request.GET.get("out_trade_no")
        total_amout = request.GET.get("total_amount")

        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status","") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break
            # 继续执行
            sleep(3)
            print("not paid...")

        context = {
            "order_sn":order_sn,
            "total_amount":total_amout,
        }
        if paid is False:
            # 支付失败
            context['result'] = "支付失败"
        else:
            # 支付成功
            context['result'] = "支付成功"

        return render(request, "shopping_car/pay.html", context=context)

class Notify(View):
    def post(self, request):
        # 查询订单是否交易成功
        # 构造支付请求
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()

        # 初始化对象
        alipay = AliPay(
            appid="2016092400582468",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 获取订单编号
        order_sn = request.POST.get('out_trade_no')
        order = Order.objects.get(order_sn=order_sn)
        # check order status
        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        # 修改订单状态
        if paid is True:
            # 支付成功
            order.order_status = 1
            order.save()

        return HttpResponse("success")