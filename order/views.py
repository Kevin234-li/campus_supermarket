from datetime import datetime
import json

from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from campus_supermarket.settings import MEDIA_URL
from goods.models import GoodsInfo
from order.models import OrderItem, OrderInfo
from user.models import User


# Create your views here.

def list_cart(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    order_items = OrderItem.objects.filter(user_id=user_id, order_pay='0')
    goods_list = []
    for item in order_items:
        goods = GoodsInfo.objects.get(id=item.goods_id)
        goods.num = item.goods_num
        goods.item_id = item.id
        goods_list.append(goods)
    return render(request, 'list_order.html',
                  {'goods_list': goods_list, 'user': user, 'num': len(goods_list), 'MEDIA_URL': MEDIA_URL})


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
    return redirect(reverse('goods:index'))


def delete_cart(request):
    id = request.GET.get("id")
    item = OrderItem.objects.get(id=id)
    item.delete()
    return redirect(reverse('order:list_cart'))


def add_order(request):
    if request.method == "GET":
        count = int(request.GET.get("count"))
        list = range(count)
        return render(request, 'add_order.html', {'list': list, 'count': count})
    elif request.method == "POST":
        text = request.POST.get("text")
        d = json.loads(text)
        user = User.objects.get(id=request.session['user_id'])
        order = OrderInfo()
        order.user = user
        order.order_date = str(datetime.now())[:8]
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
            order_item.order_pay = '1'
            order_item.save()
        order.save()
        print(d)
        return redirect(reverse('order:list_cart'))


def list_order(request):
    user_id = request.session.get('user_id')
    orders = OrderInfo.objects.filter(user_id=user_id)
    order_group = []
    for order in orders:
        order_items = OrderItem.objects.filter(order_id=order.id)
        goods_list = []
        for order_item in order_items:
            goods = GoodsInfo.objects.get(id=order_item.goods_id)
            goods.num = order_item.goods_num
            goods.pay = goods.num * goods.goods_price
            goods_list.append(goods)
        order_group.append(goods_list)
    return render(request, 'list_order.html', {"order_group": order_group, 'MEDIA_URL': MEDIA_URL})
