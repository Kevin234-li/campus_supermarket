from datetime import datetime
import json

from django.conf.urls import url
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from campus_supermarket.settings import MEDIA_URL
from goods.models import GoodsInfo
from order.models import OrderItem, OrderInfo
from user.models import User


# Create your views here.


class Order:
    def __init__(self, goods_list, desc):
        self.goods_list = goods_list
        self.desc = desc


def list_cart(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    order_items = OrderItem.objects.filter(user_id=user_id, order_pay='0')
    num = len(order_items)
    goods_list = []
    for item in order_items:
        goods = GoodsInfo.objects.get(id=item.goods_id)
        goods.num = item.goods_num
        goods.item_id = item.id
        goods_list.append(goods)
    return render(request, 'user/list_cart.html',
                  {'goods_list': goods_list, 'user': user, 'num': num, 'MEDIA_URL': MEDIA_URL})


def add_cart(request):
    try:
        order_item = OrderItem.objects.get(user_id=request.session.get('user_id'), goods_id=request.GET.get('gid'),
                                           order_pay="0")
        order_item.goods_num += int(request.GET.get('num'))
    except:
        order_item = OrderItem()
        order_item.goods_id = request.GET.get('gid')
        order_item.user_id = request.session.get('user_id')
        order_item.goods_num = request.GET.get('num')
    order_item.save()
    return redirect(reverse('order:list_cart'))


def delete_cart(request):
    id = request.GET.get("id")
    item = OrderItem.objects.get(id=id)
    item.delete()
    return redirect(reverse('order:list_cart'))


def add_order(request):
    if request.method == "POST":
        text = request.POST.get("text")
        d = json.loads(text)
        user = User.objects.get(id=request.session['user_id'])
        if request.POST.get('status') == '0':
            goods_list = []
            total_pay = 0
            for item in d:
                goods = GoodsInfo.objects.get(id=item['id'])
                goods.num = item['num']
                goods.pay = goods.num * goods.goods_price
                total_pay += goods.pay
                goods_list.append(goods)
            count = len(goods_list)
            d = {
                'goods_list': goods_list,
                'count': count,
                'total_pay': total_pay,
                'MEDIA_URL': MEDIA_URL,
                'json': text,
                'user': user
            }
            return render(request, 'user/add_order.html', d)
        elif request.POST.get('status') == '1':
            order = OrderInfo()
            order.user = user
            order.order_date = str(datetime.now())[0:8]
            order.order_total = 0
            order.save()
            for item in d:
                order.order_total += item['price'] * item['num']
                # 库存减少
                goods = GoodsInfo.objects.get(id=item['id'])
                goods.goods_repertory -= item['num']
                goods.save()
                # 订单项设置已付
                order_item = OrderItem.objects.get(user_id=user.id, order_pay='0', goods_id=item['id'])
                order_item.order_id = order.id
                order_item.goods_num = item['num']
                order_item.order_pay = '1'
                order_item.save()
            order.save()
            return redirect(reverse('order:list_cart'))
    return redirect(reverse('goods:index'))


def list_order(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-id')
    order_group = []
    for order in orders:
        order_items = OrderItem.objects.filter(order_id=order.id)
        goods_list = []
        for order_item in order_items:
            goods = GoodsInfo.objects.get(id=order_item.goods_id)
            goods.num = order_item.goods_num
            goods.pay = goods.num * goods.goods_price
            goods_list.append(goods)
        o = Order(goods_list, order)
        order_group.append(o)
    page = request.GET.get('page_num')
    p = Paginator(order_group, 5)
    try:
        order_group = p.page(page)
    except PageNotAnInteger:
        order_group = p.page(1)
    except EmptyPage:
        order_group = p.page(p.num_pages)
    return render(request, 'user/list_order.html', {"order_group": order_group, 'user': user, 'MEDIA_URL': MEDIA_URL})
