from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from users.helper import check_login


# 注册
# def register(request):
# #     return render(request, 'users/register.html')
from users import set_password
from users.forms import RegisterModelForm, LoginModelForm
from users.models import Users


class RegisterView(View):
    def get(self,request):
        return render(request,'users/register.html')
    def post(self,request):
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
            user.password = set_password(clean_data.get('password'))
            # 保存
            user.save()

            return redirect('users:登录')
        else:
            # 不合法
            return render(request,'users/register.html',context={'form':form})


# 登录
# def login(request):
#     return render(request, 'users/login.html')
class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
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
            request.session.set_expiry(0)  # 关闭浏览器session消失
            return redirect('index')
        else:
            return render(request,'users/login.html',context={'form':form})

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
    return render(request,'users/collect-edit.html')


# 全部订单
# ^allorder/$
@check_login
def allorder(request):
    return render(request, 'users/allorder.html')


# 个人资料
# ^infor/$
@check_login
def infor(request):
    # if request.method == 'POST':
    #     pass
    # else:
    #     user = Users.objects.get(phoneNum=phone)
    #     context = {
    #         'user':user
    #     }

    return render(request, 'users/infor.html')


# 确认订单
@check_login
def tureorder(request):
    return render(request, 'users/tureorder.html')

# 完成支付
@check_login
def pay(request):
    return render(request,'users/pay.html')


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

# 忘记密码
@check_login
def forgetpassword(request):
    return render(request,'users/forgetpassword.html')
