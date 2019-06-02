from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
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
                return render(request, 'user/index.html', {'user': user})
            else:
                msg = '用户名或密码错误'
                return render(request, 'user/login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后再登陆'
            return render(request, 'user/login.html', {'msg': msg})


def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    finally:
        return redirect(reverse('user:login'))


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    if request.method == 'POST':
        user = User()
        user.username = request.POST.get('username')
        user.password = request.POST.get('pwd')
        user.email = request.POST.get("email")
        u = User.objects.filter(username=user.username)
        e = User.objects.filter(email=user.email)
        if u:
            return render(request, 'user/register.html', {'msg1': "用户名已存在！"})
        elif e:
            return render(request, 'user/register.html', {'msg2': "邮箱已被占用！"})
        else:
            user.save()
            return redirect(reverse('user:login'))


def profile(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    return render(request, 'user/usercenter.html', {"user": user})


def edit(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    user.password = request.POST.get("pwd")
    user.phone = request.POST.get("phone")
    user.email = request.POST.get("email")
    user.direction = request.POST.get("direction")
    user.save()
    return render(request, 'user/usercenter.html', {"user": user})


def basic_info(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session.get('user_id'))
        return render(request, 'user/basic_info.html', {'user': user})
    elif request.method == 'POST':
        pass


def account_security(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session.get('user_id'))
        return render(request, 'user/account_security.html', {'user': user})
    elif request.method == 'POST':
        pass


def address(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session.get('user_id'))
        return render(request, 'user/address.html', {'user': user})
    elif request.method == 'POST':
        pass

