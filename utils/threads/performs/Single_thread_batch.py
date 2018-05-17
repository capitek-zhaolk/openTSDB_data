#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: test1.py

@time: 2018/5/15/015 14:59

@desc:
'''
import time
import math
import requests
import json
import copy
import random
import simplejson


# 数据逐条插入数据库
# 使用批量处理




# list保存响应时间
res_times=[]

# 数据库返回success、failed
return_list = []

class SignleThreads:
    def __init__(self, content):
        self.count = 0
        self.content = content

    def sendJson(self):
        start_time_res = time.time()
        s = requests.Session()
        r = s.post("http://172.17.0.239:4242/api/put?details", json=self.content)
        self.count += 1
        return_list.append(r.text)
        end_time_res = time.time()
        res_times.append(end_time_res - start_time_res)

        return r.text, self.count


def _run(nums):
    flag = True
    new_result = []
    success_nums = 0
    totals = 0
    failed_nums = 0
    json_list = []
    global stats, end

    while flag:

        stats = time.time()
        a = int(time.time())
        for i in range(1, nums + 1):
            end = time.time()
            json = {
                "metric": "sys.batch.danxiancheng",
                "timestamp": a,
                "value": 1234,
                "tags": {
                    "username": "zhaolk_566"
                }
            }
            a += 0.5
            json_list.append(json)
            if len(json_list) == 50:
                results = SignleThreads(json_list)
                results = results.sendJson()
                new_result.append(results)
                json_list = []

            if end - stats >= 1:
                print u'开始时间是{0}'.format(stats)
                print u'结束时间是{0}'.format(end)

                print u'在{0}秒的时间内'.format(end - stats)
                flag = False
                break


    for ins in range(len(new_result)):
        new_ = new_result[ins][0]
        new_ = new_.encode('utf-8')
        new_ = eval(new_)
        for k, v in new_.items():
            if k == 'success':
                single_success_nums = int(v)
                success_nums += int(v)
            if k == 'failed':
                single_failed_nums = int(v)
                failed_nums += int(v)

    for ins in range(len(new_result)):
        totals += new_result[ins][1]

    print '访问HTTP Post方法{0}次'.format(totals)

    print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (nums, success_nums, end - stats, success_nums, failed_nums))



if __name__ == '__main__':
    nums = 20000

    while True:
        _run(nums)