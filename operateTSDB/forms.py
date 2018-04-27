#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: forms.py

@time: 2018/4/10/010 11:44

@desc:
'''

from django import forms

class InputForm(forms.Form):
    username=forms.CharField(required=True)
    start_time=forms.CharField(required=True)
    end_time=forms.CharField(required=True)