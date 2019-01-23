


# 建立一个模型基础类,让所有的模型都能继承
from django.db import models


class BaseModel(models.Model):
    # 额外字段
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        # 设置当前类为抽象的类,被迁移
        abstract = True