from django.conf.urls import url
from . import views

app_name = 'wechat'

urlpatterns = [
    url(r'^wechat/index$', views.wechat, name='wechat'),
    url(r'^wechat/index1$', views.index1, name='index1'),
    url(r'^wechat/index2$', views.index2, name='index2'),
]