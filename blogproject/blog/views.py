# coding:utf-8
import markdown
from markdown.extensions.toc import TocExtension

from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

# from comments.forms import CommentForm
from .models import Post, Category


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


# # 详情页视图函数
# def detail(request, pk):
#
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views_num()
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         TocExtension(slugify=slugify),
#     ])
#     post.content = md.convert(post.content)
#     return render(request, 'blog/detail.html', {'post': post, 'toc': md.toc})


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):

        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views_num()

        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        #post.body = md.convert(post.body)
        post.content = md.convert(post.content)
        post.toc = md.toc
        return post










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
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                                    created_time__month=month
                                                                )

# 分类页

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
















# # 归档页（时间）
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list': post_list})
#
#
# # 分类页
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})