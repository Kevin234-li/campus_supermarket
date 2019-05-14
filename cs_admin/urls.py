from django.conf.urls import url

from cs_admin import views

app_name = 'cs_admin'
urlpatterns = [
    # 登录
    url(r'^login/', views.login, name='login'),
    # 后台首页
    url(r'^index/', views.index, name='index'),
    # 增加商品
    url(r'^add_goods/', views.add_goods, name='add_goods'),
    # 编辑商品
    url(r'^edit_goods/', views.edit_goods, name='edit_goods'),
    # 删除商品
    url(r'^delete_goods', views.delete_goods, name='delete_goods'),
    # 添加管理员
    url(r'add_admin/', views.add_admin, name='add_admin'),
]

