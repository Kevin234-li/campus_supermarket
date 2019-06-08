import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from campus_supermarket.settings import MEDIA_URL
from cs_admin.models import Admin
from goods.models import GoodsInfo, GoodsCategory
from order.models import OrderInfo, OrderItem
from user.models import User
from datetime import date, datetime
import calendar
import json



def list_goods(request):
    if request.method == "GET":
        admin = Admin.objects.get(id=request.session["admin_id"])
        goods_list = GoodsInfo.objects.all().order_by('id')
        p = Paginator(goods_list, 10)
        page = request.GET.get('page_num')
        try:
            goods_list = p.page(page)
        except PageNotAnInteger:
            goods_list = p.page(1)
        except EmptyPage:
            goods_list = p.page(p.num_pages)
        return render(request, "admin/goods/list_goods.html",
                      {'goods_list': goods_list, "MEDIA_URL": MEDIA_URL, "admin": admin})


def add_goods(request):
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/goods/add_goods.html', {"cags": cags})
    if request.method == 'POST':
        goods = GoodsInfo()
        goods.goods_name = request.POST.get('goods_name')
        goods.goods_num = request.POST.get('goods_num')
        goods.goods_manufacturer = request.POST.get('goods_manufacturer')
        goods.goods_price = request.POST.get('goods_price')
        goods.goods_unit = request.POST.get('goods_unit')
        goods.goods_repertory = request.POST.get('goods_repertory')
        kind = request.POST.get('kind')
        goods.cag = GoodsCategory.objects.get(cag_name=kind)
        goods.goods_img = request.FILES.get("g_img")
        goods.save()
        return redirect(reverse("cs_admin:list_goods"))


def edit_goods(request):
    gid = request.GET.get('gid')
    goods = GoodsInfo.objects.get(id=gid)
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/goods/edit_goods.html', {'goods': goods, "cags": cags})
    if request.method == 'POST':
        goods.goods_name = request.POST.get('goods_name')
        goods.goods_num = request.POST.get('goods_num')
        goods.goods_manufacturer = request.POST.get('goods_manufacturer')
        goods.goods_price = request.POST.get('goods_price')
        goods.goods_unit = request.POST.get('goods_unit')
        goods.goods_repertory = request.POST.get('goods_repertory')
        kind = request.POST.get('kind')
        goods.cag = GoodsCategory.objects.get(cag_name=kind)
        img = request.FILES.get("g_img")
        if img:
            goods.goods_img = img
        goods.save()
        return redirect(reverse("cs_admin:list_goods"))


def edit_goods2(request):
    return render(request, 'admin/goods/edit_goods2.html')


def delete_goods(request):
    gid = request.GET.get('gid')
    goods = GoodsInfo.objects.get(id=gid)
    goods.delete()
    return render(request, 'admin/index.html')


def add_admin(request):
    if request.method == 'GET':
        return render(request, 'admin/add_admin.html', {'msg': ""})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_c = request.POST.get('password_c')
        # 验证参数都不能为空
        if not all([username, password, password_c]):
            return render(request, 'admin/add_admin.html', {'msg': '请填写完整的信息'})
        if Admin.objects.filter(username=username):
            return render(request, 'admin/add_admin.html', {'msg': '用户名已存在！'})
        if password != password_c:
            return render(request, 'user/register.html', {'msg': '两次密码不一致'})
        Admin.objects.create(username=username, password=password, )
        return render(request, 'admin/index.html')


def list_admin(request):
    admins = Admin.objects.all()
    return render(request, 'admin/list_admin.html', {'admins': admins})


def edit_admin(request):
    if request.method == "GET":
        return render(request, 'admin/edit_admin.html')
    elif request.method == "POST":
        admin_id = request.POST.get("admin_id")
        admin = Admin.objects.get(id=admin_id)
        old_pwd = request.POST.get("old_pwd")
        if old_pwd != admin.password:
            return HttpResponse("false")
        else:
            admin.password = request.POST.get("new_pwd")
            admin.save()
            return redirect(reverse('cs_admin:list_admin'))


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username)
        print(password)
        if Admin.objects.filter(username=username):
            admin = Admin.objects.get(username=username)
            # 验证密码是否正确
            if password == admin.password:
                request.session["admin_id"] = admin.id
                return HttpResponse("登录成功！")
            else:
                return HttpResponse("用户名或密码错误!")
        else:
            return HttpResponse("用户名不存在!")


def logout(request):
    try:
        del request.session['admin_id']
    except:
        pass
    finally:
        return redirect(reverse('cs_admin:login'))


# 分类管理
def list_cag(request):
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/cag/list_cag.html', {'cags': cags, 'MEDIA_URL': MEDIA_URL})


def add_cag(request):
    if request.method == 'GET':
        return render(request, 'admin/cag/add_cag.html')
    elif request.method == 'POST':
        cag = GoodsCategory()
        cag.cag_name = request.POST.get('cag_name')
        img = request.FILES.get('cag_img')
        if img:
            cag.cag_img = img
        cag.save()
        return redirect(reverse('cs_admin:list_cag'))


def edit_cag(request):
    if request.method == 'GET':
        cag_id = request.GET.get("cag_id")
        cag = GoodsCategory.objects.get(id=cag_id)
        return render(request, 'admin/cag/edit_cag.html', {'cag': cag})
    elif request.method == 'POST':
        cag_id = request.GET.get("cag_id")
        print(cag_id)
        cag = GoodsCategory.objects.get(id=cag_id)
        cag.cag_name = request.POST.get('cag_name')
        cag_img = request.FILES.get('cag_img')
        if cag_img:
            cag.cag_img = cag_img
        cag.save()
        return redirect(reverse('cs_admin:list_cag'))


# 订单管理
def list_order(request):
    orders = OrderInfo.objects.all().order_by('-order_date')
    p = Paginator(orders, 15)
    page = request.GET.get("page_num")
    try:
        orders = p.page(page)
        for order in orders:
            user = User.objects.get(id=order.user_id)
            order.client_name = user.username
            order.client_phone = user.phone
    except PageNotAnInteger:
        orders = p.page(1)
    except EmptyPage:
        orders = p.page(p.num_pages)
    return render(request, 'admin/order/list_order.html', {'orders': orders})


def order_detail(request):
    order_id = request.GET.get("oid")
    order = OrderInfo.objects.get(id=order_id)
    user = User.objects.get(id=order.user_id)
    order.client_name = user.username
    goods_list = []
    order_items = OrderItem.objects.filter(order_id=order_id)
    for item in order_items:
        goods = GoodsInfo.objects.get(id=item.goods_id)
        goods.goods_num = item.goods_num
        goods.goods_pay = goods.goods_num * goods.goods_price
        goods.goods_cag_name = GoodsCategory.objects.get(id=goods.cag_id).cag_name
        goods_list.append(goods)
    return render(request, 'admin/order/order_detail.html',
                  {"goods_list": goods_list, "order": order, 'MEDIA_URL': MEDIA_URL})


def sale_statistic(request):
    cur_date = datetime.now()
    orders = OrderInfo.objects.filter(order_date__gte=date(cur_date.year, cur_date.month - 1, 1),
                                      order_date__lte=date(cur_date.year, cur_date.month, 1))
    data1 = [0] * (calendar.monthrange(cur_date.year, cur_date.month - 1))[1]
    data2 = {}
    data3 = {}
    for order in orders:
        data1[order.order_date.day - 1] += float(order.order_total)
        order_items = OrderItem.objects.filter(order_id=order.id)
        for item in order_items:
            goods = GoodsInfo.objects.get(id=item.goods_id)
            goods.sale_num = item.goods_num
            goods.pay = item.goods_num * goods.goods_price
            goods.cag_name = GoodsCategory.objects.get(id=goods.cag_id).cag_name
            if goods.goods_name in data2.keys():
                data2[goods.goods_name] += goods.sale_num
            else:
                data2[goods.goods_name] = goods.sale_num
            if goods.cag_name in data3.keys():
                data3[goods.cag_name] += goods.pay
            else:
                data3[goods.cag_name] = goods.pay
    data2 = sorted(data2.items(), key=lambda x: x[1], reverse=True)
    total_sale = sum(v for k, v in data3.items())
    t = sorted(data3.items(), key=lambda x: x[1], reverse=True)
    data3 = []
    for i in range(6):
        data3.append({"name": t[i][0], "y": t[i][1] / total_sale * 100})
    d = {
        "data1": json.dumps(data1),
        "data2_keys": json.dumps([k[0] for i, k in enumerate(data2, 1) if i <= 10]),
        "data2_values": json.dumps([k[1] for i, k in enumerate(data2, 1) if i <= 10]),
        "data3": json.dumps(data3),
        "total_sale": total_sale
    }
    return render(request, 'admin/goods/sale_statistic.html', d)


# 用户管理
def list_user(request):
    users = User.objects.all().order_by("id")
    return render(request, 'admin/client/list_user.html', {"users": users})


def edit_user(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        user = User.objects.get(id=user_id)
        redirect(reverse('cs_admin:edit_user'))
        return render(request, 'admin/client/edit_user.html', {"user": user})
    elif request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        user.username = request.POST.get("username") if request.POST.get("username") else user.username
        user.nickname = request.POST.get("nickname") if request.POST.get("nickname") else user.nickname
        user.gender = request.POST.get("gender") if request.POST.get("gender") else user.gender
        user.birth_date = request.POST.get("birth_date") if request.POST.get("birth_date") else user.birth_date
        user.phone = request.POST.get("phone") if request.POST.get("phone") else user.phone
        user.email = request.POST.get("email") if request.POST.get("email") else user.email
        user.save()
        return list_user(request)


def buy_history(request):
    if request.method == "GET":
        return render(request, 'admin/client/buy_history.html')


def buy_history2(request):
    user_id = request.GET.get("client_id")
    page = request.GET.get("page_num")
    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-order_date')
    p = Paginator(orders, 15)
    try:
        orders = p.page(page)
        for order in orders:
            user = User.objects.get(id=order.user_id)
            order.client_id = user_id
            order.client_name = user.username
            order.client_phone = user.phone
    except PageNotAnInteger:
        orders = p.page(1)
    except EmptyPage:
        orders = p.page(p.num_pages)
    return render(request, 'admin/client/buy_history2.html', {"orders": orders, "client_id": user_id})


def search(request):
    question = request.GET.get("question")
    goods_list = GoodsInfo.objects.filter(Q(goods_name__icontains=question)
                                          | Q(goods_manufacturer__icontains=question)
                                          )
    user_list = User.objects.filter(Q(username__contains=question)
                                    | Q(nickname__icontains=question)
                                    | Q(password__icontains=question))
    order_list = None
    if re.match("\\d{4}-\\d{2}-\\d{2}", question):
        y, m, d = map(int, question.split("-"))
        order_list = OrderInfo.objects.filter(order_date__day=d, order_date__month=m, order_date__year=y)
        for order in order_list:
            user = User.objects.get(id=order.user_id)
            order.user = user
    return render(request, 'admin/show.html',
                  {"goods_list": goods_list, "user_list": user_list, "order_list": order_list})
