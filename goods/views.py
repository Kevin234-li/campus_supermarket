from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from campus_supermarket.settings import MEDIA_URL
from goods.models import GoodsInfo, GoodsCategory
from user.models import User


class Cag_Goods:
    def __init__(self, cag, goods_list):
        self.cag = cag
        self.goods_list = goods_list


def index(request):
    user = None
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        pass
    cag_list = GoodsCategory.objects.all()
    cag_goods_list = []
    for cag in cag_list:
        goods_list = GoodsInfo.objects.filter(cag_id=cag.id)[:4]
        g = Cag_Goods(cag, goods_list)
        cag_goods_list.append(g)
    return render(request, 'user/index.html', {'user': user, 'cag_goods_list': cag_goods_list,  'MEDIA_URL': MEDIA_URL})


def show(request):
    content = request.GET.get('content')
    if content:
        request.session["last_search"] = content
    else:
        content = request.session["last_search"]
    page = request.GET.get('page_num')
    goods_list = GoodsInfo.objects.filter(Q(goods_name__icontains=content)
                                          | Q(goods_manufacturer__icontains=content)
                                          )
    num = len(goods_list)
    p = Paginator(goods_list, 10)
    try:
        goods_list = p.page(page)
    except PageNotAnInteger:
        goods_list = p.page(1)
    except EmptyPage:
        goods_list = p.page(p.num_pages)
    user = None
    try:
        user = User.objects.get(id=request.session.get('user_id'))
    except:
        pass
    return render(request, 'user/show.html', {'goods_list': goods_list, 'user': user, 'num': num, 'MEDIA_URL': MEDIA_URL})


def goods_detail(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    goods_id = request.GET.get('gid')
    goods = GoodsInfo.objects.get(id=goods_id)
    goods.cag_name = GoodsCategory.objects.get(id=goods.cag_id).cag_name
    return render(request, 'user/goods/goods_detail.html', {'goods': goods, "user": user, "MEDIA_URL": MEDIA_URL})
