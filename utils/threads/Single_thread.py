#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: Single_thread.py

@time: 2018/4/26/026 14:41

@desc:
'''

# 单线程

import time
import math
import requests
import json
import copy
import random
import simplejson


def send_json(jsons, s):
    r = s.post("http://172.17.0.239:4242/api/put?details", json=jsons)
    # print '发送的result是{0} 类型是{1}'.format(r.text, type(r.text))
    return r.text


def testcase1(nums):
    startt = time.time()
    prevt = time.time()
    s = requests.Session()
    json_list = []
    new_result = []
    ry = []

    success_nums = 0
    single_success_nums = 0
    failed_nums = 0
    single_failed_nums = 0

    success_num = 0
    single_success_num = 0
    failed_num = 0
    single_failed_num = 0

    for i in range(1,nums+1):

        a = int(time.time())
        v = int(1234567)
        json = {
            "metric": "sys.batch.danxiancheng",
            "timestamp": a,
            "value": v,
            "tags": {
                "host": "web36",
                "dc": "lgas36"
            }
        }
        json_list.append(json)

        if len(json_list) == 50:
            ry.append(i)
            midt = time.time()
            results = send_json(json_list, s)
            results = results.encode('utf-8')
            es = time.time()
            res = eval(results)
            new_result.append(res)
            json_list = []

    for ins in range(len(new_result)):

        for k, v in new_result[ins].items():
            if k == 'success':
                single_success_nums = int(v)
                success_nums += int(v)
            if k == 'failed':
                single_failed_nums = int(v)
                failed_nums += int(v)
        print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (nums, single_success_nums, es - midt, single_success_nums, single_failed_nums))
        time.sleep(0.05)



    start_ry = time.time()
    # print '域外的i是{0}'.format(i%50)
    results = send_json(json_list, s)
    results = results.encode('utf-8')
    end_ry = time.time()
    res = eval(results)
    # print '域外的res是{0}'.format(res)
    for k, v in res.items():
        if k == 'success':
            single_success_num = int(v)
            success_num += int(v)
        if k == 'failed':
            single_failed_num = int(v)
            failed_num += int(v)


    json_list = []
    # print 'ry是%s' % ry[-1]
    print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (nums, (i%50), end_ry - start_ry, single_success_num, single_failed_num))



    end_success = success_num + success_nums
    end_failed = failed_num + failed_nums
    t = 0.05 * len(new_result)
    end_times = time.time()
    print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (nums, nums, end_times - startt - t, end_success, end_failed))



if __name__ == '__main__':


    #testcase1(100)

    # testcase1(101)

    testcase1(10000)
