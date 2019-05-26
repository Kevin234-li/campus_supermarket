from django.conf.urls import url

from goods import views

app_name = 'goods'

urlpatterns = [
    # url(r'/', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^show/', views.show, name='show'),
    url(r'^goods_detail/', views.goods_detail, name='goods_detail'),

]