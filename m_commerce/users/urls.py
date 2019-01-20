from django.conf.urls import url

from users.views import RegisterView, LoginView, personal_center, my_wallet, gladdress, address, collect, allorder, \
    infor, \
    integral, integralexchange, integralrecords, job, mymessage, myrecommend, recommend, records, saftystep, step, ygq, \
    yhq, tureorder, forgetpassword,collect_edit

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name="注册"),
    url(r'^login/$', LoginView.as_view(), name="登录"),
    url(r'^personal_center/$', personal_center, name="个人中心"),
    url(r'^my_wallet/$', my_wallet, name="我的钱包"),
    url(r'^gladdress/$', gladdress, name="管理收货地址"),
    url(r'^address/$', address, name="增加收货地址"),
    url(r'^collect/$', collect, name="我的收藏"),
    url(r'^collect_edit/$', collect_edit, name='收藏编辑'),
    url(r'^allorder/$', allorder, name="全部订单"),
    url(r'^tureorder/$', tureorder, name="确认订单"),
    url(r'^infor/$', infor, name="个人资料"),
    url(r'^integral/$', integral, name="积分"),
    url(r'^integralexchange/$', integralexchange, name="积分兑换"),
    url(r'^integralrecords/$', integralrecords, name="兑换记录"),
    url(r'^job/$', job, name="我要兼职"),
    url(r'^mymessage/$', mymessage, name="我的动态"),
    url(r'^myrecommend/$', myrecommend, name="我的推荐"),
    url(r'^recommend/$', recommend, name='推荐有奖'),
    url(r'^records/$', records, name='账户余额'),
    url(r'^saftystep/$', saftystep, name='安全设置'),
    url(r'^step/$', step, name='系统设置'),
    url(r'^ygq/$', ygq, name='已过期的红包'),
    url(r'^yhq/$', yhq, name='可使用的红包'),
    url(r'^forgetpassword/$', forgetpassword, name='忘记密码'),


]
