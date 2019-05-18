from django.db import models

# Create your models here.


class OrderInfo(models.Model):
    # order_id = models.CharField(max_length=20, primary_key=True)        # 订单id
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)    # 关联用户
    order_date = models.DateTimeField(auto_now=True)                    # 购买日期
    order_pay = models.BooleanField(default=False)                      # 付款属性
    order_total = models.DecimalField(max_digits=6, decimal_places=2)   # 总价
    # order_address = models.CharField(max_length=150)                    # 收货地址
    class Meta:
        db_table = 'orderinfo'

class OrderItem(models.Model):
    order_id = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)   #订单id
    goods_id = models.ForeignKey('goods.GoodsInfo', on_delete=models.CASCADE)
    goods_num = models.IntegerField()
    class Meta:
        db_table = 'order_item'

