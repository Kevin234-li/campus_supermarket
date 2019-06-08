from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)      # 用户名
    nickname = models.CharField(max_length=32)  # 昵称
    password = models.CharField(max_length=256)                  # 密码
    email = models.CharField(max_length=64, unique=True)         # 邮箱
    gender = models.CharField(max_length=10)  # 性别
    birth_date = models.DateField(max_length=32)  # 出生日期
    phone = models.CharField(max_length=11, default='')          # 收件人电话
    direction = models.CharField(max_length=100, default='')     # 收货地址

    class Meta:
        db_table = 'user'
