from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


# 注册
# def register(request):
# #     return render(request, 'users/register.html')
class RegisterView(View):
    def get(self,request):
        return render(request,'users/register.html')
    def post(self,request):
        pass


# 登录
# def login(request):
#     return render(request, 'users/login.html')
class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        pass

# 个人中心
def personal_center(request):
    return render(request, 'users/member.html')


# 我的钱包
# ^my_wallet/$
def my_wallet(request):
    return render(request, 'users/money.html')


# 管理收货地址
# ^gladdress/$
def gladdress(request):
    return render(request, 'users/gladdress.html')


# 增加收货地址
# ^address/$
def address(request):
    return render(request, 'users/address.html')


# 我的收藏
# ^collect/$
def collect(request):
    return render(request, 'users/collect.html')


# 全部订单
# ^allorder/$
def allorder(request):
    return render(request, 'users/allorder.html')


# 个人资料
# ^infor/$
def infor(request):
    return render(request, 'users/infor.html')


# 确认订单
def tureorder(request):
    return render(request, 'users/tureorder.html')


# 积分
# ^integral/$
def integral(request):
    return render(request, 'users/integral.html')


# 积分兑换
# ^integralexchange/$
def integralexchange(request):
    return render(request, 'users/integralexchange.html')


# 兑换记录
# ^integralrecords/$
def integralrecords(request):
    return render(request, 'users/integralrecords.html')


# 我要兼职
def job(request):
    return render(request, 'users/job.html')


# 我的动态
# ^mymessage/$
def mymessage(request):
    return render(request, 'users/mymessage.html')


# 我的推荐
def myrecommend(request):
    return render(request, 'users/myrecommend.html')


# 推荐有奖
def recommend(request):
    return render(request, 'users/recommend.html')


# 账户余额
def records(request):
    return render(request, 'users/records.html')


# 安全设置
def saftystep(request):
    return render(request, 'users/saftystep.html')


# 系统设置
def step(request):
    return render(request, 'users/step.html')


# 我的红包  ---- 已过期
def ygq(request):
    return render(request, 'users/ygq.html')


# 我的红包 ---可使用
def yhq(request):
    return render(request, 'users/yhq.html')

# 忘记密码
def forgetpassword(request):
    return render(request,'users/forgetpassword.html')
