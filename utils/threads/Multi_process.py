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
import sys

from time import sleep

total = None
# list保存响应时间
res_times=[]

# 数据库返回success、failed
return_list = []

def send_json(jsons):
    with requests.Session() as session:
        start_time_res = time.time()
        r = session.post("http://172.17.0.239:4242/api/put?details", json=jsons, headers={'Connection':'close'})
        return_list.append(r.text)
        end_time_res = time.time()
        res_times.append(end_time_res - start_time_res)
        return r


def testcase1(nums):
    global process_name, total
    total = 0
    time_response = []
    try:

        process_name = multiprocessing.current_process().name
        a = int(time.time())
        json = {
            "metric": "sys.batch.duojincheng",
            "timestamp": a,
            "value": math.sin(nums) + 0.15,
            "tags": {
                "name": "zhaolk_mutil14"
            }
        }
        t = send_json(json)
        # t.elapsed.total_seconds()  # 获取响应时间
        total = total + 1
        time_response.append(t.elapsed.total_seconds())
        return t.text, total, time_response
    except Exception as e:
        print e
        sleep(2.5)

    finally:
        pass


if __name__ == '__main__':

    total_nums = 10000
    multi_process_nums =10
    # multiprocessing.Pool 创建子进程
    pool = multiprocessing.Pool(multi_process_nums)

    single_success_num = 0
    single_failed_num = 0
    success_num = 0
    failed_num = 0
    total = 0
    res_times = []

    start_time = time.time()

    result = pool.map(testcase1, [i for i in range(0, total_nums)])

    for ins in enumerate(result):
        total += int(ins[1][1])
        res_times.append(ins[1][2][0])

        res = ins[1][0].decode('gb2312').encode('utf-8')
        res_dict = eval(res)
        for k, v in res_dict.items():
            if k == 'success':
                single_success_num = int(v)
                success_num += int(v)
            if k == 'failed':
                single_failed_num = int(v)
                failed_num += int(v)

    end_time = time.time()

    print '在{0}秒内，一共访问HTTP Post方法{1}次，每秒访问{2}次，平均响应时间是{3} sec'.format(end_time-start_time, total, int(total / (end_time-start_time)), sum(res_times)/len(res_times))
    print '发送{0}条数据，分为{1}个进程，耗时{2} sec , success {3}次 , failed {4}次 '.format(total_nums, multi_process_nums, end_time-start_time, success_num, failed_num)
    pool.close()
    pool.join()





