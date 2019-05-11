from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)      # 用户名
    password = models.CharField(max_length=256)                  # 密码
    password_c = models.CharField(max_length=256)                # 确认密码
    email = models.CharField(max_length=64, unique=True)         # 邮箱
    recipients = models.CharField(max_length=10, default='')     # 收件人姓名
    phone = models.CharField(max_length=11, default='')          # 收件人电话
    addressee_p = models.CharField(max_length=6, default='')     # 收件人邮编
    direction = models.CharField(max_length=100, default='')     # 收件人地址

