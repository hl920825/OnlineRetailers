from users import set_password
from users.models import Users
from django import forms

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
            raise forms.ValidationError({'repassword':"两次密码不一致!"})
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

class RegisterModelForm(forms.ModelForm):
    "注册表单类模型"
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required':'必须填写密码',
                                   'min_length':"密码至少为8位",
                                   'max_length':'密码最多为16位',
                               })
    repassword = forms.CharField(error_messages={'required': '必须填写密码'})
    class Meta:
        model = Users
        fields = ['phoneNum']
        error_messages = {
            'phoneNum':{
                'required':'手机号必须填写'
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
    def clean(self):
        # 判断两次密码输入是否一致
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({'repassword':"两次密码不一致!"})
        else:
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
        fields =['phoneNum']

        error_messages = {
            'phoneNum':{
                'required':'手机号必须填写'
            }
        }
    def clean(self):
        # 验证手机号
        phoneNum = self.cleaned_data.get('phoneNum')
        # 查询数据库
        try:
            user = Users.objects.get(phoneNum=phoneNum)
        except Users.DoesNotExist:
            raise forms.ValidationError({'phoneNum':'手机号不存在'})

        # 验证密码
        password = self.cleaned_data.get('password','')
        if user.password != set_password(password):
            raise forms.ValidationError({'password':'密码错误'})

        # 返回所有清洗后的数据
        self.cleaned_data['user'] = user
        return self.cleaned_data


