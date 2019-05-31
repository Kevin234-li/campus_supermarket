from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        data = {}
        # 验证信息是否填写完整
        if not all([username, password]):
            data['msg'] = '请填写完整的用户名或密码'
        # 验证用户是否注册
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # 验证密码是否正确
            if password == user.password:
                request.session['user_id'] = user.id
                redirect(reverse('goods:index'))
                return render(request, 'index.html', {'user': user})
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后再登陆'
            return render(request, 'login.html', {'msg': msg})


def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    finally:
        return redirect(reverse('user:login'))


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password_c = request.POST.get('cpwd')
        email = request.POST.get('email')
        # 验证参数都不能为空
        if not all([username, password, password_c, email]):
            data = {
                'msg': '请填写完整的信息'
            }
            return render(request, 'register.html', data)
        if password != password_c:
            data = {
                'msg': '两次密码不一致'
            }
            return render(request, 'register.html', data)
        # 加密password
        # 创建用户并添加到数据库
        User.objects.create(username=username,
                            password=password,
                            email=email)
        # 注册成功跳转到登陆页面
        return HttpResponseRedirect(reverse('user:login'))


def profile(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    return render(request, 'usercenter.html', {"user": user})


def edit(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    user.password = request.POST.get("pwd")
    user.phone = request.POST.get("phone")
    user.email = request.POST.get("email")
    user.direction = request.POST.get("direction")
    user.save()
    return render(request, 'usercenter.html',{"user": user})