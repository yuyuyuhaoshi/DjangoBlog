# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

"""
使用下方的模板引擎方式。
def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
"""


#使用下方真正的首页视图函数
def index(request):
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
"""
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""