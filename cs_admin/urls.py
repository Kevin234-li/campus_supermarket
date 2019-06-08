from django.conf.urls import url

import goods
from cs_admin import views

app_name = 'cs_admin'
urlpatterns = [
    # 登录
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    # 商品管理
    url(r'^list_goods/', views.list_goods, name='list_goods'),
    url(r'^add_goods/', views.add_goods, name='add_goods'),
    url(r'^edit_goods/$', views.edit_goods, name='edit_goods'),
    url(r'^edit_goods2/$', views.edit_goods2, name='edit_goods2'),
    url(r'^delete_goods/', views.delete_goods, name='delete_goods'),
    # 管理员管理
    url(r'^add_admin/', views.add_admin, name='add_admin'),
    url(r'^list_admin/', views.list_admin, name='list_admin'),
    url(r'^edit_admin/', views.edit_admin, name='edit_admin'),
    # 分类管理
    url(r'^list_cag/$', views.list_cag, name='list_cag'),
    url(r'^add_cag/$', views.add_cag, name='add_cag'),
    url(r'^edit_cag/$', views.edit_cag, name='edit_cag'),
    # 订单管理
    url(r'^list_order/$', views.list_order, name='list_order'),
    url(r'^order_detail/$', views.order_detail, name='order_detail'),
    url(r'^sale_statistic/$', views.sale_statistic, name='sale_statistic'),
    # 用户管理
    url(r'^list_user/$', views.list_user, name='list_user'),
    url(r'^edit_user/', views.edit_user, name='edit_user'),
    url(r'^buy_history/$', views.buy_history, name='buy_history'),
    url(r'^buy_history2/', views.buy_history2, name='buy_history2'),
    # 搜索
    url(r'^search/', views.search, name='search')
]

