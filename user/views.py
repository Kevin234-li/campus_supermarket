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
        print(username)
        print(password)
        # 验证用户是否注册
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # 验证密码是否正确
            if password == user.password:
                request.session['user_id'] = user.id
                return HttpResponse("登录成功！")
            else:
                return HttpResponse("用户名或密码错误！")
        else:
            return HttpResponse("用户名不存在,请注册后再登陆!")


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
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get("email")
        if User.objects.filter(username=username):
            return HttpResponse("用户名已被占用！")
        if User.objects.filter(email=email):
            return HttpResponse("邮箱已被占用！")
        User.objects.create(username=username, password=password, email=email)
        return HttpResponse("注册成功！请返回登录")


def basic_info(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session.get('user_id'))
        return render(request, 'user/user_center/basic_info.html', {'user': user})
    elif request.method == 'POST':
        pass


def edit_basic_info(request):
    user = User.objects.get(id=request.session.get('user_id'))
    if request.method == "GET":
        return render(request, 'user/user_center/edit_basic_info.html', {'user': user})
    elif request.method == "POST":
        user.username = request.POST.get("username") if request.POST.get("username") else user.username
        user.nickname = request.POST.get("nickname") if request.POST.get("nickname") else user.nickname
        user.gender = request.POST.get("gender") if request.POST.get("gender") else user.gender
        user.birth_date = request.POST.get("birth_date") if request.POST.get("birth_date") else user.birth_date
        user.phone = request.POST.get("phone") if request.POST.get("phone") else user.phone
        user.email = request.POST.get("email") if request.POST.get("email") else user.email
        user.save()
        redirect(reverse('user:basic_info'))
        return render(request, 'user/user_center/basic_info.html', {'user': user})


def account_security(request):
    user = User.objects.get(id=request.session.get('user_id'))
    if request.method == 'GET':
        return render(request, 'user/user_center/account_security.html', {'user': user})
    elif request.method == 'POST':
        old_pwd = request.POST.get("old_pwd")
        if old_pwd != user.password:
            return HttpResponse("false")
        else:
            user.password = request.POST.get("new_pwd")
            user.save()
            return render(request, 'user/user_center/account_security.html', {'user': user})


def address(request):
    user = User.objects.get(id=request.session.get('user_id'))
    if request.method == 'GET':
        return render(request, 'user/user_center/address.html', {'user': user})
    elif request.method == 'POST':
        user.direction = request.POST.get("address");
        user.save()
        return render(request, 'user/user_center/address.html', {'user': user})
