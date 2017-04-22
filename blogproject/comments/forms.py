#!/usr/bin/env python3
# encoding: utf-8

"""
@version: 1.0.0
@author: Haoshi YU
@license: None
@file: forms.py
@time: 2017/4/22 13:07
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "名字",
            }),
            'email': forms.TextInput(attrs={
                'placeholder': "邮箱",
            }),
            'url': forms.TextInput(attrs={
                'placeholder': "网站",
            }),
        }
