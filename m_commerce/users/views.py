import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View
from users.helper import check_login, send_sms, login
from users import set_password
from users.forms import RegisterModelForm, LoginModelForm, ForgetModelForm, ChangeModelForm
from users.models import Users
from django_redis import get_redis_connection


# 发送手机验证码
class SendMessage(View):
    def get(self, request):
        pass

    def post(self, request):
        # 1 接收参数
        phoneNum = request.POST.get('phoneNum', '')
        rs = re.search('^1[3-9]\d{9}$', phoneNum)
        # 验证参数合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errMsg': '手机号码格式错误!'})
        # 2.处理数据

        # 模拟
        # 生成随机验证码
        # 保存验证码到redis中,存取速度快,并且可以方便的销毁时间
        # 接入运营商

        # 生成随机验证码   字符串
        random_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        print('=========随机验证码为{}========'.format(random_code))

        # 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(phoneNum, random_code)
        # 设置60秒后过期
        r.expire(phoneNum, 60)

        # 首先获取当前手机号码的发送次数
        key_times = '{}_times'.format(phoneNum)
        now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # now_times = now_times.decode('utf-8') # 正常转换方式
        # now_times = int(now_times)
        # if now_times is None or int(now_times) < 5:
        #     # 保存手机发送验证码的次数,不能超过5次
        #     r.incr(key_times)
        #     # 设置一个过期时间
        #     r.expire(key_times,60) # 3600
        # else:
        #     # 返回 告知用户发送次数过多
        #     return JsonResponse({'error':1,'errMsg':'发送次数过多!'})

        # 接入运营商
        # >>>3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"黄豆豆是大傻子大超市\"}" % random_code
        # print(params)
        rs = send_sms(__business_id, phoneNum, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 3.合成响应
        return JsonResponse({'error': 0})


# def sendMessage(request):
#     try:
#         # 获取手机号码
#         phoneNum = request.GET.get('phoneNum')
#         # 验证手机号是否正确
#         phoneNum_re = re.compile('^1[3-9]\d{9}$')
#         res = re.search(phoneNum_re,phoneNum)
#         if res:
#             # 生成随机验证码
#             code = ''.join([str(random.randint(0,9)) for _ in range(4)])
#             # 保存到session中,等验证的时候使用
#             request.session['session_code'] = code
#             # 设置过期时间
#             request.session.set_expiry(60*60)
#             print(code)
#             print('================')
#
#
#     except:
#         return {'ok':0,'code':500,'msg':'短信验证码发送失败'}

# 注册
# def register(request):
# #     return render(request, 'users/register.html')
class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证参数合法性
        form = RegisterModelForm(data)
        if form.is_valid():
            # 操作数据库
            clean_data = form.cleaned_data
            #
            user = Users()
            user.phoneNum = clean_data.get('phoneNum')
            # 加密
            user.password = set_password(clean_data.get('password'))
            # 保存
            user.save()

            return redirect('users:登录')
        else:
            # 不合法
            return render(request, 'users/register.html', context={'form': form})


# 登录
# def login(request):
#     return render(request, 'users/login.html')
class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证合法性
        form = LoginModelForm(data)
        if form.is_valid():
            # 验证成功
            # 保存登录标识到session中
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['phoneNum'] = user.phoneNum
            request.session['head'] = user.head
            request.session.set_expiry(0)  # 关闭浏览器session消失
            return redirect('index')
        else:
            return render(request, 'users/login.html', context={'form': form})


# 个人中心
@check_login
def personal_center(request):
    return render(request, 'users/member.html')


# 我的钱包
# ^my_wallet/$
@check_login
def my_wallet(request):
    return render(request, 'users/money.html')


# 管理收货地址
# ^gladdress/$
@check_login
def gladdress(request):
    return render(request, 'users/gladdress.html')


# 增加收货地址
# ^address/$
@check_login
def address(request):
    return render(request, 'users/address.html')


# 我的收藏
# ^collect/$
@check_login
def collect(request):
    return render(request, 'users/collect.html')


# 收藏编辑
@check_login
def collect_edit(request):
    return render(request, 'users/collect-edit.html')


# 全部订单
# ^allorder/$
@check_login
def allorder(request):
    return render(request, 'users/allorder.html')


# 个人资料
# ^infor/$
@check_login
def infor(request):
    if request.method == 'POST':
        # 获取数据修改数据库
        user_id = request.session.get("ID")
        head = request.FILES.get('head')
        nickName = request.POST.get("nickName")
        gender = request.POST.get("gender")
        school = request.POST.get("school")
        home_address = request.POST.get("home_address")
        detail_address = request.POST.get("detail_address")
        birthday = request.POST.get('birthday')

        # 先保存图片
        user = Users.objects.get(pk=user_id)
        if head is not None:
            user.head = head
            user.save()
        # 修改数据库
        Users.objects.filter(id=user_id).update(nickName=nickName,
                                           gender=gender,
                                           school=school,
                                            birthday=birthday,
                                           home_address=home_address,
                                           detail_address=detail_address)
        user = Users.objects.get(pk=user_id)
        # 同时修改session
        login(request,user)

        return redirect("users:个人中心")

    else:
        # 通过session得到用户信息
        user_id = request.session.get("ID")
        # 到数据库中查询用户信息
        user_info = Users.objects.filter(id=user_id).first()
        # print(user_info)
        context = {
            "user": user_info
        }

        return render(request, 'users/infor.html', context=context)


# 忘记密码
def forgetpassword(request):
    if request.method == "POST":
        # 接收参数
        data = request.POST
        # phoneNum = data.get('phoneNum')
        # 验证参数合法性
        form = ForgetModelForm(data)
        if form.is_valid():
            # 操作数据库
            cleaned_data = form.cleaned_data

            # user = Users()
            # user.phoneNum = clean_data.get('phoneNum')
            # 加密
            password = set_password(cleaned_data.get('password'))
            # # 修改
            res = Users.objects.filter(id=cleaned_data.get("id")).update(password=password)
            # if res:
            #     # 跳转回登录
            return redirect('users:登录')
            # return redirect('users:忘记密码')
        else:
            # 不合法
            return render(request, 'users/forgetpassword.html', context={'form': form})
    else:
        # 通过session得到用户信息
        user_id = request.session.get('ID')
        # 到数据库中查询用户信息
        user_info = Users.objects.filter(id=user_id).first()
        context = {
            'user': user_info
        }
        return render(request, 'users/forgetpassword.html', context=context)


# 确认订单
@check_login
def tureorder(request):
    return render(request, 'users/tureorder.html')

# 再次确认
def order(request):
    return render(request,'users/order.html')


# 完成支付
@check_login
def pay(request):
    return render(request, 'users/pay.html')


# 积分
# ^integral/$
@check_login
def integral(request):
    return render(request, 'users/integral.html')


# 积分兑换
# ^integralexchange/$
@check_login
def integralexchange(request):
    return render(request, 'users/integralexchange.html')


# 兑换记录
# ^integralrecords/$
@check_login
def integralrecords(request):
    return render(request, 'users/integralrecords.html')


# 我要兼职
@check_login
def job(request):
    return render(request, 'users/job.html')


# 我的动态
# ^mymessage/$
@check_login
def mymessage(request):
    return render(request, 'users/mymessage.html')


# 我的推荐
@check_login
def myrecommend(request):
    return render(request, 'users/myrecommend.html')


# 推荐有奖
@check_login
def recommend(request):
    return render(request, 'users/recommend.html')


# 账户余额
@check_login
def records(request):
    return render(request, 'users/records.html')


# 安全设置
@check_login
def saftystep(request):
    return render(request, 'users/saftystep.html')


# 修改密码
@check_login
def changePassword(request):
    if request.method == 'POST':
        # 接收数据
        data = request.POST
        # 清洗数据
        form = ChangeModelForm(data)
        # 验证合法性
        if form.is_valid():
            # 获得清洗后的数据
            # cleaned_data = form.cleaned_data
            # 保存数据库
            newpassword = form.cleaned_data.get('newpassword1')
            newpassword1 = set_password(newpassword)
            Users.objects.filter(pk=form.cleaned_data.get('user_id')).update(password=newpassword1)
            request.session.flush()
            return redirect('users:登录')
        else:
            errors = form.errors
            context = {
                "errors": errors
            }
            return render(request, 'users/password.html', context=context)
    else:
        return render(request, 'users/password.html')

# 绑定新手机号
def boundphone(request):
    return render(request,'users/boundphone.html')


# 系统设置
@check_login
def step(request):
    return render(request, 'users/step.html')


# 我的红包  ---- 已过期
@check_login
def ygq(request):
    return render(request, 'users/ygq.html')


# 我的红包 ---可使用
@check_login
def yhq(request):
    return render(request, 'users/yhq.html')

# 安全退出
def safquit(request):
    request.session.flush()
    return render(request,'users/login.html')
