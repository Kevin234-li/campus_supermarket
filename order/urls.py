from django.conf.urls import url

from order import views

app_name = 'order'

urlpatterns = [
    url(r'cart/', views.cart, name='cart')
]