#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: Multi_process.py

@time: 2018/4/26/026 14:41

@desc:
'''


# 多进程

import threading
import multiprocessing
import time
import math
import requests
import json
import copy
import random
import simplejson

def send_json(jsons, s):
    r = s.post("http://172.17.0.239:4242/api/put?details", json=jsons)
    return r.text


def testcase1(nums):

    process_name = multiprocessing.current_process().name
    # print nums, process_name
    s = requests.Session()
    a = int(time.time())
    json = {
        "metric": "sys.batch.duoxiancheng",
        "timestamp": a,
        "value": int(5467829),
        "tags": {
            "name": "zhaolk_serverd27_2"
        }
    }
    t = send_json(json, s)

    # print '名称是{0} 数据是{1}'.format(process_name, nums)
    return t

if __name__ == '__main__':
    total_nums = 222
    thread_nums = 20
    pool = multiprocessing.Pool(thread_nums)

    single_success_num = 0
    single_failed_num = 0
    success_num = 0
    failed_num = 0

    start_time = time.time()
    result = pool.map(testcase1, [i for i in range(1, total_nums+1)])
    for idx, ele in enumerate(result):
        ele = ele.encode('gbk')
        ele = eval(ele)
        for k, v in ele.items():
            if k == 'success':
                single_success_num = int(v)
                success_num += int(v)
            if k == 'failed':
                single_failed_num = int(v)
                failed_num += int(v)
    end_time = time.time()
    print '发送{0}条数据，分为{1}个线程，耗时{2} sec , success {3}次 , failed {4}次 '.format(total_nums, thread_nums, end_time-start_time, success_num, failed_num)
    pool.close()
    pool.join()





