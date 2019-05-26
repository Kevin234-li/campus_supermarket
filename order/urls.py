from django.conf.urls import url

from order import views

app_name = 'order'

urlpatterns = [
    url(r'list_order/', views.list_order, name='list_order'),
    url(r'list_cart/', views.list_cart, name='list_cart'),
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^delete_cart/', views.delete_cart, name='delete_cart'),
    url(r'^add_order/', views.add_order, name='add_order'),
]