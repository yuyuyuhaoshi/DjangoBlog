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

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects,all()[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_times', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.all()
