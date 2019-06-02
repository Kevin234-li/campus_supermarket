from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from campus_supermarket.settings import MEDIA_URL
from cs_admin.models import Admin
from goods.models import GoodsInfo, GoodsCategory


def profile(request):
    id = request.GET.get('id')
    admin = Admin.objects.get(id=id)
    return render(request, 'admin/profile.html', {'admin': admin})
    pass


def logout(request):
    return render(request, 'admin/login.html')


def list_goods(request):
    if request.method == "GET":
        goods_list = GoodsInfo.objects.all().order_by('cag_id')
        p = Paginator(goods_list, 10)
        page = request.GET.get('page_num')
        try:
            goods_list = p.page(page)
        except PageNotAnInteger:
            goods_list = p.page(1)
        except EmptyPage:
            goods_list = p.page(p.num_pages)
        return render(request, 'admin/list_goods.html', {'goods_list': goods_list, "MEDIA_URL": MEDIA_URL})


def add_goods(request):
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/add_goods.html', {"cags": cags})
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
        return render(request, 'admin/index.html')


def edit_goods(request):
    gid = request.GET.get('gid')
    goods = GoodsInfo.objects.get(id=gid)
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/edit_goods.html', {'goods': goods, "cags": cags})
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
        return render(request, 'admin/index.html')


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
        Admin.objects.create(username=username, password=password,)
        return render(request, 'admin/index.html')


def list_admin(request):
    admins = Admin.objects.all()
    return render(request, 'admin/list_admin.html', {'admins': admins})

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
                # return HttpResponseRedirect(reverse('cs_admin:index'))
                return HttpResponseRedirect(reverse('cs_admin:index2'))
            else:
                msg = '用户名或密码错误'
                return render(request, 'admin/login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后再登陆'
            return render(request, 'admin/login.html', {'msg': msg})

# 后台首页


def index(request):
    return render(request, 'admin/index.html')


# 分类管理
def list_cag(request):
    if request.method == 'GET':
        cags = GoodsCategory.objects.all()
        return render(request, 'admin/list_cag.html', {'cags': cags, 'MEDIA_URL': MEDIA_URL})


def add_cag(request):
    if request.method == 'GET':
        return render(request, 'admin/add_cag.html')
    elif request.method == 'POST':
        cag = GoodsCategory()
        cag.cag_name = request.POST.get('cag_name')
        cag.cag_img = request.FILES.get('cag_img')
        cag.save()
        return redirect(reverse('cs_admin:list_cag'))


def edit_cag(request):
    if request.method == 'GET':
        cag_id = request.GET.get("cag_id")
        cag = GoodsCategory.objects.get(id=cag_id)
        return render(request, 'admin/edit_cag.html', {'cag': cag})
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
