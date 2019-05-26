from django.conf.urls import url
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from goods.models import GoodsInfo
from user.models import User


def index(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        return redirect(reverse('user:login'))
    return render(request, 'index.html', {'user': user})


def show(request):
    content = request.GET.get('content')
    result = GoodsInfo.objects.filter(Q(goods_name__icontains=content) | Q(goods_manufacturer__icontains=content))
    user = User.objects.get(id=request.session.get('user_id'))
    return render(request, 'show.html', {'goods_list': result, 'user': user, 'num': len(result)})


def goods_detail(request):
    goods_id = request.GET.get('gid')
    goods = GoodsInfo.objects.get(id=goods_id)
    return render(request, 'goods_detail.html', {'goods': goods})


