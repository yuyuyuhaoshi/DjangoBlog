#!/usr/bin/env python3
# encoding: utf-8

"""
@version: 1.0.0
@author: Haoshi YU
@license: None
@file: blog_tags.py
@time: 2017/4/17 22:38
"""
from django import template
from ..models import Post, Category
from django.db.models.aggregates import Count


register = template.Library()


# 显示五篇最近的文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


# 归档 按插入时间降序排列
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post'))
