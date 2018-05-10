#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: opentsdb_duoxiancheng.py

@time: 2018/5/8/008 8:36

@desc:
'''

import threading
import time
import math
import requests

# list保存响应时间
res_times=[]

# 数据库返回success、failed
return_list = []

class ThreadCuts(threading.Thread):
    def __init__(self, content):
        threading.Thread.__init__(self)
        self.content = content
        self.count = 0

    def sendJson(self, c):
        start_time_res = time.time()
        s = requests.Session()
        r = s.post("http://172.17.0.239:4242/api/put?details", json=c)
        return_list.append(r.text)
        end_time_res = time.time()
        res_times.append(end_time_res - start_time_res)
        return r.text

    def run(self):
        global thread_lock
        while True:
            thread_lock.acquire()
            length = len(content)
            if length >0:
                tmp = content.pop()
                # print self.getName(), tmp
                self.sendJson(tmp)
                self.count += 1
                thread_lock.release()
            else:
                thread_lock.release()
                break
            time.sleep(0.01)

if '__main__' == __name__:

    global thread_lock

    start_time = time.time()

    content = []
    total_nums = 1000
    a = int(time.time())
    for ins in range(1, total_nums+1):
        json = {
            "metric": "sys.batch.test.mutileThreads",
            "timestamp": a,
            "value": math.sin(ins) + 0.205,
            "tags": {
                "name": "zhaolk_51"
            }
        }
        a += 0.5
        content.append(json)

    thread_lock = threading.RLock()

    # thread_nums = 10
    thread_nums = 20


    threads = []
    all_count = 0
    for ins in range(thread_nums):
        thread = ThreadCuts(content)
        threads.append(thread)

    for x in range(len(threads)):
        threads[x].start()

    for y in range(len(threads)):
        threads[y].join()

    for xx in threads:
        all_count += xx.count


    single_success_nums = 0
    single_failed_nums = 0
    success_nums = 0
    failed_nums = 0

    for xxx in range(len(return_list)):
        resu = return_list[xxx].encode('utf-8')
        for k, v in eval(resu).items():
            if k == 'success':
                single_success_nums = int(v)
                success_nums += int(v)
            if k == 'failed':
                single_failed_nums = int(v)
                failed_nums += int(v)

    end_time = time.time()

    print '在{0}秒内，一共访问HTTP Post方法{1}次，Request/Second {2}次/sec，平均响应时间是{3} sec'.format(end_time-start_time, all_count, int(all_count / (end_time-start_time)), sum(res_times)/len(res_times))
    print '{0} thread，Total data {1}，time consuming {2} sec'.format(thread_nums, total_nums, end_time-start_time)
    print 'success {0}次 ， failed {1}次'.format(success_nums, failed_nums)
