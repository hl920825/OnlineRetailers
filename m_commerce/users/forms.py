from django.core.validators import RegexValidator

from indent.models import UserAddress
from users import set_password
from users.models import Users
from django import forms
from django_redis import get_redis_connection


class ForgetModelForm(forms.ModelForm):
    # 忘记密码模型
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': "密码至少为8位",
                                   'max_length': '密码最多为16位',
                               })
    repassword = forms.CharField(error_messages={'required': '必须填写密码'})

    def clean(self):
        # 判断两次密码输入是否一致
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({'repassword': "两次密码不一致!"})
        else:
            return self.cleaned_data

    class Meta:
        model = Users
        fields = ['password']

    def clean_password(self):
        # 数据库中查询密码
        password = self.cleaned_data.get('password')
        password1 = set_password(password)
        flag = Users.objects.filter(password=password1).exists()
        if flag:
            # 存在
            raise forms.ValidationError('密码未修改,请重新输入')
        return password


# 修改密码表单类模型
class ChangeModelForm(forms.ModelForm):
    user_id = forms.CharField()
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': "密码至少为8位",
                                   'max_length': '密码最多为16位',
                               })
    newpassword1 = forms.CharField(max_length=16,
                                   min_length=8,
                                   error_messages={
                                       'required': '必须填写密码',
                                       'min_length': "密码至少为8位",
                                       'max_length': '密码最多为16位',
                                   })
    newpassword2 = forms.CharField(error_messages={'required': '必须填写密码'})

    class Meta:
        model = Users
        fields = ['password', 'user_id']

    def clean(self):
        user_id = self.cleaned_data.get('user_id')
        password = self.cleaned_data.get('password', '')
        password2 = set_password(password)
        rs = Users.objects.get(id=user_id)
        if rs.password != password2:
            raise forms.ValidationError({'password': "原始密码错误"})
        # 验证两个新密码是否一致
        pwd1 = self.cleaned_data.get('newpassword1')
        pwd2 = self.cleaned_data.get('newpassword2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            # 两次密码不同错误
            raise forms.ValidationError({'newpassword2': '两次密码输入不相同'})
        # 返回清洗后的数据
        return self.cleaned_data


class RegisterModelForm(forms.ModelForm):
    "注册表单类模型"
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': "密码至少为8位",
                                   'max_length': '密码最多为16位',
                               })
    repassword = forms.CharField(error_messages={'required': '必须填写密码'})
    # 验证码
    captcha = forms.CharField(max_length=6, error_messages={
        'required': '验证码必须填写'
    })
    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议'
    })

    class Meta:
        model = Users
        fields = ['phoneNum']
        error_messages = {
            'phoneNum': {
                'required': '手机号必须填写'
            }
        }
        # 验证手机号是否存在

    def clean_phoneNum(self):
        phoneNum = self.cleaned_data.get('phoneNum')
        flag = Users.objects.filter(phoneNum=phoneNum).exists()
        if flag:
            # 存在
            raise forms.ValidationError('该手机号已注册,请重新填写')
        return phoneNum

        # 验证用户传入的验证码和redis中的是否一样

    def clean(self):
        # 判断两次密码输入是否一致
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({'repassword': "两次密码不一致!"})

        # 综合校验
        try:
            captcha = self.cleaned_data.get('captchar')
            phoneNum = self.cleaned_data.get('phoneNum', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(phoneNum)  # 二进制  转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({'captcha': '验证码输入错误!'})
        except:
            raise forms.ValidationError({'captcha': '验证码输入错误!'})

        # 返回清洗后的数据
        return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    # 登录表单模型
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': "密码至少为8位",
                                   'max_length': '密码最多为16位',
                               })

    class Meta:
        model = Users
        fields = ['phoneNum']

        error_messages = {
            'phoneNum': {
                'required': '手机号必须填写'
            }
        }

    def clean(self):
        # 验证手机号
        phoneNum = self.cleaned_data.get('phoneNum')
        # 查询数据库
        try:
            user = Users.objects.get(phoneNum=phoneNum)
        except Users.DoesNotExist:
            raise forms.ValidationError({'phoneNum': '手机号不存在'})

        # 验证密码
        password = self.cleaned_data.get('password', '')
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码错误'})

        # 返回所有清洗后的数据
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 收货地址验证
class AddressAddForm(forms.ModelForm):

    phone = forms.CharField(error_messages={'required':'请填写正确手机号码!'},
                            min_length=11,
                            required=True,
                            validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号码格式不正确')])
    class Meta:
        model = UserAddress
        exclude = ['add_time','change_time','is_delete','user']
        error_messages = {
            'username': {
            "required":"请填写用户名!",
            },
            'brief':{
                'required':"请填写详细地址!",
            },
            'hproper':{
                "required":"请填写完整地址!",
            },
            'hcity': {
                "required": "请填写完整地址!",
            },
            'harea': {
                "required": "请填写完整地址!",
            },
        }

    # def clean(self):
    #     # 验证如果数据库里地址已经超过6报错
    #     cleaned_data = self.cleaned_data
    #     count = UserAddress.objects.filter(user_id=self.data.get("user_id")).count()
    #     if count >= 6:
    #         raise forms.ValidationError({"hproper": "收货地址最多只能保存6条"})
    #
    #     # 设置默认
    #     if cleaned_data.get('isDefault'):
    #         UserAddress.objects.filter(user=self.data.get("user_id")).update(isDefault=False)
    #
    #     return cleaned_data
