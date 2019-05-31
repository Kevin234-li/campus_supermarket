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
    # 档案
    url(r'profile/', views.profile, name='profile'),
    # 编辑
    url(r'edit/', views.edit, name='edit'),
]