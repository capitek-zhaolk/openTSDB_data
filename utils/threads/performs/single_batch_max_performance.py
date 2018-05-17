#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: single_batch_max_performance.py

@time: 2018/5/17 14:59

@desc:
'''
import time
import math
import requests
import json
import copy
import random
import simplejson


# 数据插入数据库
# 批量处理
# 1秒钟调用Http Post 的次数
# 1秒钟写入数据库的数据量


# list保存响应时间
# res_times=[]

# 数据库返回success、failed
return_list = []

class SignleThreads:
    def __init__(self, content):
        self.count = 0
        self.content = content

    def sendJson(self):
        # start_time_res = time.time()
        s = requests.Session()
        r = s.post("http://172.17.0.239:4242/api/put?details", json=self.content)
        self.count += 1
        return_list.append(r.text)
        # end_time_res = time.time()
        # res_times.append(end_time_res - start_time_res)
        return r.text, self.count


def _run(nums):
    new_result = []
    success_nums = 0
    totals = 0
    totalss = 0
    failed_nums = 0
    json_list = []
    _line = 100
    global stats, end

    stats = time.time()
    a = int(time.time())
    _starts = time.time()
    # print u'start time {0}'.format(_starts)
    a = 1526400000
    for i in xrange(1, nums + 1):
        json = {
            "metric": "singleThreads",
            "timestamp": a,
            "value": 1111,
            "tags": {
                "username": "zhaolk_14"
            }
        }
        a += 1
        json_list.append(json)
        if len(json_list) == 50:
            _start_hu = time.time()
            results = SignleThreads(json_list)
            results = results.sendJson()
            totalss += 1
            _end_hu = time.time()

            if totalss % _line == 0:
                print u'每调用Http Post {0}次， 需耗时{1}秒'.format(_line, (_end_hu-_start_hu)*_line)
                _start_hu = _end_hu

            new_result.append(results)
            json_list = []

        _ends = time.time()
        if _ends - _starts >= 1:
            print u'程序总共运行了{0}'.format(_ends - _starts)
            break


    for ins in range(len(new_result)):
        new_ = new_result[ins][0]
        new_ = new_.encode('utf-8')
        new_ = eval(new_)
        for k, v in new_.items():
            if k == 'success':
                success_nums += int(v)
            if k == 'failed':
                failed_nums += int(v)

    for ins in range(len(new_result)):
        totals += new_result[ins][1]
    end = time.time()
    print u'总共访问HTTP Post方法{0}次'.format(totals)

    print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (nums, success_nums, end - stats, success_nums, failed_nums))



if __name__ == '__main__':
    nums = 50000

    while True:
        _run(nums)