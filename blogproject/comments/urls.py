#!/usr/bin/env python3
# encoding: utf-8

"""
@version: ??
@author: Haoshi YU
@license: None
@file: url.py
@time: 2017/4/22 14:08
"""

from django.conf.urls import url
from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]