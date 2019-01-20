from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

# Create your models here.

class Users(models.Model):
    gender_choices = (
        (1,'男'),
        (2,'女'),
        (3,'保密'),
    )
    phoneNum = models.CharField(max_length=11,
                                verbose_name='手机号',
                                validators=[
                                    RegexValidator(r'^1[3-9]\d{9}$','手机号码格式错误')
                                ])
    nickName = models.CharField(max_length=16,null=True,
                                verbose_name='昵称',
                                validators=[
                                    MinLengthValidator(2,'昵称至少为2个字符')
                                ])
    password = models.CharField(max_length=32)
    gender = models.SmallIntegerField(choices=gender_choices,default=3)
    school = models.CharField(max_length=200,null=True,verbose_name="学校名称")
    home_address = models.CharField(max_length=200,null=True,verbose_name="老家地址")
    detail_address = models.CharField(max_length=200,null=True,verbose_name='现住地址')
    birthday = models.DateField(null=True,verbose_name='生日日期')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    change_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    # head = models.ImageField(upload_to='head/%Y%m',default='head/hlwtx.jpg',verbose_name='用户头像')

    def __str__(self):
        return self.phoneNum
    class Meta:
        db_table = 'users'