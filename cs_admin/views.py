from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from cs_admin.models import Admin


def profile(request):
    pass


def logout(request):
    pass

def add_goods(request):
    pass

def edit_goods(request):
    pass

def delete_goods(request):
    pass

def add_admin(request):
    pass

# 登录

def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        # 验证信息是否填写完整
        if not all([username, password]):
            data['msg'] = '用户名或者密码不能为空'
        # 验证用户是否注册
        if Admin.objects.filter(username=username).exists():
            admin = Admin.objects.get(username=username)
            # 验证密码是否正确
            if password == admin.password:
                return HttpResponseRedirect(reverse('cs_admin:index'))
            else:
                msg = '用户名或密码错误'
                return render(request, 'admin/login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后再登陆'
            return render(request, 'admin/login.html', {'msg': msg})

# 后台首页


def index(request):
    return render(request, 'admin/index.html')
