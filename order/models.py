from django.db import models

# Create your models here.


class OrderInfo(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)     # 关联用户
    order_date = models.DateTimeField(auto_now=True)                    # 购买日期
    order_total = models.DecimalField(max_digits=6, decimal_places=2)   # 总价

    class Meta:
        db_table = 'orderinfo'


class OrderItem(models.Model):
    order_id = models.IntegerField()  # 订单id
    user_id = models.IntegerField()   # 用户id
    # goods = models.ForeignKey('goods.GoodsInfo', on_delete=models.CASCADE)
    goods_id = models.IntegerField()
    goods_num = models.IntegerField()
    order_pay = models.BooleanField(default=False)                      # 付款属性

    class Meta:
        db_table = 'order_item'

