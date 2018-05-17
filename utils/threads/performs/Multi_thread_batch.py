#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: Multi_thread_batch.py

@time: 2018/5/15/015 18:09

@desc:
'''

# 使用多线程 + 批量处理
# 测试在一秒钟内传入数据库的数据量


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
            length = len(self.content)
            if length >0:
                tmp = self.content.pop()
                print self.getName(), len(tmp)
                self.sendJson(tmp)
                self.count += 1
                thread_lock.release()
            else:
                thread_lock.release()
                break
            time.sleep(0.01)

def _run(thread_nums, content):
    threads = []
    all_count = 0

    success_nums = 0
    failed_nums = 0

    try:
        for ins in range(thread_nums):
            thread = ThreadCuts(content)
            threads.append(thread)
    except Exception as e:
        print e

    try:

        for x in range(len(threads)):
            threads[x].start()

        for y in range(len(threads)):
            threads[y].join()

        for xx in threads:
            all_count += xx.count
    except Exception as e:
        print e

    for xxx in range(len(return_list)):
        resu = return_list[xxx].encode('utf-8')
        for k, v in eval(resu).items():
            if k == 'success':
                single_success_nums = int(v)
                success_nums += int(v)
            if k == 'failed':
                single_failed_nums = int(v)
                failed_nums += int(v)

    return all_count, success_nums, failed_nums


if '__main__' == __name__:

    global stats, end, thread_lock

    thread_lock = threading.RLock()

    total_nums = 10000000

    thread_nums = 2
    flag = True
    success_nums = 0
    failed_nums = 0
    content = []
    json_list = []

    while flag:

        stats = time.time()
        a = int(time.time())
        for ins in range(1, total_nums + 1):
            end = time.time()
            json = {
                "metric": "sys.batch.test.mutileThreads",
                "timestamp": a,
                "value": math.sin(ins) + 0.305,
                "tags": {
                    "name": "zhaolk_60"
                }
            }
            a += 0.5
            json_list.append(json)
            if len(json_list) == 50:
                content.append(json_list)
                json_list = []

            if end - stats >= 1:
                print '时间是{0}'.format(end-stats)
                print u'开始时间是{0}'.format(stats)
                print u'结束时间是{0}'.format(end)

                print u'在{0}秒的时间内'.format(end - stats)
                flag = False
                break


    print 'content数据是{0} -- {1}'.format(len(content), len(content)*50)
    resu = _run(thread_nums, content)

    # for ins in range(len(resu)):
    print '访问HTTP Post方法{0}次'.format(resu[0])

    print('Total data %d, Send %d data use times %f sec, success %d 次 , failed %d 次 ' % (
    total_nums, resu[1], end - stats, resu[1], resu[2]))

