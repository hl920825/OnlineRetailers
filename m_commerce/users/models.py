from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

class Users(models.Model):
    gender_choices = (
        (1,'男'),
        (2,'女'),
        (3,'保密'),
    )
    phoneNum = models.CharField(max_length=11,
                                validators=[
                                    MinLengthValidator(11,'手机号应为11位')
                                ])
    nickName = models.CharField(max_length=16,null=True,
                                validators=[
                                    MinLengthValidator(2,'昵称至少为2个字符')
                                ])
    password = models.CharField(max_length=32)
    gender = models.SmallIntegerField(choices=gender_choices,default=3)
    school = models.CharField(max_length=200,null=True)
    home_address = models.CharField(max_length=200,null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.phoneNum
    class Meta:
        db_table = 'users'