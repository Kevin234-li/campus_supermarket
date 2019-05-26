from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from goods.models import GoodsInfo
from order.models import OrderItem
from user.models import User

# Create your views here.


def list_order(request):
    pass


def list_cart(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    order_items = OrderItem.objects.filter(user_id=user_id)
    goods_list = []
    for item in order_items:
        goods = GoodsInfo.objects.get(id=item.goods_id)
        goods.num = item.goods_num
        goods.item_id = item.id
        goods_list.append(goods)
    return render(request, 'list_cart.html', {'goods_list': goods_list, 'user': user, 'num': len(goods_list)})


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
    return HttpResponse("hello")
