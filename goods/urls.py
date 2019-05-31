from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve

from campus_supermarket import settings
from campus_supermarket.settings import MEDIA_ROOT
from goods import views

app_name = 'goods'

urlpatterns = [
    # url(r'/', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^show/', views.show, name='show'),
    url(r'^goods_detail/', views.goods_detail, name='goods_detail'),
]