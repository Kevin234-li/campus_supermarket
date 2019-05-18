from django.db import models

# Create your models here.


class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=20)  # 商品名称
    goods_img = models.ImageField(upload_to='shop')  # 商品图片
    goods_num = models.IntegerField()  # 商品货号
    goods_price = models.FloatField(default=0)  # 商品价格
    goods_unit = models.CharField(max_length=20, default='500g')  # 商品单位
    goods_manufacturer = models.CharField(max_length=50)  # 生产厂家
    goods_repertory = models.IntegerField()  # 商品库存
    cag = models.ForeignKey('GoodsCategory', on_delete=models.CASCADE)
    class Meta:
        db_table = 'goodsinfo'

class GoodsCategory(models.Model):
    cag_name = models.CharField(max_length=100)
    # cag_css = models.CharField(max_length=20)
    cag_img = models.ImageField(upload_to='cag')
    class Meta:
        db_table = 'goods_category'

