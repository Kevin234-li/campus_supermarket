from django.conf.urls import url

from user import views

app_name = 'user'
urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登陆
    url(r'^login/', views.login, name='login'),
    # 退出
    url(r'^logout/', views.logout, name='logout'),
    # 编辑
    url(r'^basic_info/$', views.basic_info, name='basic_info'),
    url(r'^edit_basic_info/$', views.edit_basic_info, name='edit_basic_info'),
    url(r'^account_security/$', views.account_security, name='account_security'),
    url(r'^address/$', views.address, name='address'),

]