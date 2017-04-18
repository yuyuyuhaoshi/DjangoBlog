# coding:utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
import markdown

"""
使用下方的模板引擎方式。
def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
"""


# 首页视图函数

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

# 详情页视图函数
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.content = markdown.markdown(post.content,
    #                                  extensions=[
    #                                      'markdown.extensions.extra',
    #                                      'markdown.extensions.codehilite',
    #                                      'markdown.extensions.toc',
    #                                  ])
    return render(request, 'blog/detail.html', context={'post': post})
