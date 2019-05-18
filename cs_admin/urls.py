from django.conf.urls import url

import goods
from cs_admin import views

app_name = 'cs_admin'
urlpatterns = [
    # 登录
    url(r'^login/', views.login, name='login'),
    # 后台首页
    url(r'^index/', views.index, name='index'),
    url(r'^index2/', views.index2, name='index2'),
    # 商品列表
    url(r'^list_goods/', views.list_goods, name='list_goods'),
    # 增加商品
    url(r'^add_goods/', views.add_goods, name='add_goods'),
    # 编辑商品
    url(r'^edit_goods/', views.edit_goods, name='edit_goods'),
    # 删除商品
    url(r'^delete_goods/', views.delete_goods, name='delete_goods'),
    # 添加管理员
    url(r'add_admin/', views.add_admin, name='add_admin'),
    # 管理员列表
    url(r'list_admin/', views.list_admin, name='list_admin'),
    # 个人中心
    url(r'profile/', views.profile, name='profile'),

]

