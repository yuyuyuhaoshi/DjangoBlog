# coding:utf-8
import markdown
from django.shortcuts import render, get_object_or_404
# from comments.forms import CommentForm
from .models import Post, Category
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
"""
使用下方的模板引擎方式。
def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
"""


# 首页视图函数
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


# 详情页视图函数
def detail(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.increase_views_num()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.content = md.convert(post.content)
    return render(request, 'blog/detail.html', {'post': post, 'toc': md.toc})
"""
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown.markdown(
                                  post.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    post.content = md.convert(post.content)
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    context = {'post': post,
               'toc': md.toc,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)
"""


# 搜索功能
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})

# 归档页（时间）
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类页
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})