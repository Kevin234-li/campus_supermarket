from django.db import models

# Create your models here.


class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=20)  # 商品名称
    goods_img = models.ImageField(upload_to='shop')  # 商品图片
    goods_price = models.FloatField(default=0)  # 商品价格
    goods_unit = models.CharField(max_length=20, default='500g')  # 商品单位
    goods_repertory = models.IntegerField()  # 商品库存
    goods_cag = models.ForeignKey('GoodsCategory', on_delete=models.CASCADE)


class GoodsCategory(models.Model):
    cag_name = models.CharField(max_length=100)
    cag_css = models.CharField(max_length=20)
    cag_img = models.ImageField(upload_to='cag')

