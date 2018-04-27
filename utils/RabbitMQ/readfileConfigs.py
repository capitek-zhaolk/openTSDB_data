#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: readfileConfigs.py

@time: 2018/3/9/009 15:27

@desc:
'''

import os, json, copy

def readFileConfigs():
    file_name_list = []
    list1 = []
    # new_dir = []
    list_dir = '/usr/local/capitek/aaa/data/server/log/radacct/acctrec/'
    file_names = os.listdir(list_dir)

    for file_name in file_names:
        oldDir = os.path.join(list_dir, file_name) # 原来文件路径
        filename = os.path.splitext(file_name)[0] # 文件名
        list1.append(str(filename))

    # 对文件进行排序
    list1.sort()

    # 完整的路径
    # news = file_name.encode('utf-8').strip()
    # file_name_list.append(os.path.join(list_dir, news))

    #for x, y in enumerate(list1):
    #    for files in file_names:
    #        filename = os.path.splitext(files)[0]  # 文件名
    #        if int(filename) == y:
    #            olddir = os.path.join(list_dir, files)
    #            newdir = os.path.join(list_dir, str(y)) # 新的文件路径
    #            new_dir = os.path.join(list_dir, files)
    #            file_name_list.append(os.path.join(list_dir, files))


    # return file_name_list
    return list1

def json_list():
    file_name_list = readFileConfigs()
    return file_name_list

json_list()













