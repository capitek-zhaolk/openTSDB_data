#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: Multi_batch_max_performance.py

@time: 2018/5/17/017 13:57

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
    def __init__(self, content, theradname):
        threading.Thread.__init__(self, name=theradname)
        self.__running = threading.Event() # 停止多线程的标识
        self.content = content
        self.count = 0
        self.counts = 0

    def sendJson(self, c):
        # start_time_res = time.time()
        s = requests.Session()
        r = s.post("http://172.17.0.239:4242/api/put?details", json=c)
        return_list.append(r.text)
        # end_time_res = time.time()
        # res_times.append(end_time_res - start_time_res)

        return r.text

    def run(self):
        for ins in xrange(len(self.content)):
            _start = time.time()
            self.sendJson(self.content[ins])
            self.count += 1
            self.counts += 1
            _end = time.time()
            if self.counts % 100 == 0:
                print u'{0} -- 每调用Http Post接口{1}次， 需耗时{2}'.format(self.name, self.counts, (_end - _start)*20)
                self.counts = 0

        # global threadLock

        # while True:

            # threadLock.acquire()
            # length = len(self.content)
            # if length > 0:
            #     tmp = self.content.pop()
            #     _start = time.time()
            #     self.sendJson(tmp)
            #     self.count += 1
            #     self.counts += 1
            #     _end = time.time()
            #     # print '线程是{0} 数据是{1}'.format(self.name, self.count)
            #     if self.counts % 100 == 0:
            #         print '{0} -- 每调用Http Post接口{1}次， 需耗时{2}'.format(self.name, self.counts, (_end - _start)*100)
            #         self.counts = 0
            #     threadLock.release()
            # else:
            #     threadLock.release()
            #     break

def _run(thread_nums, content):
    threads = []
    all_count = 0
    all_time = 1
    now_time = time.time()

    # 创建线程
    try:
        for ins in range(1, thread_nums + 1):
            thread = ThreadCuts(content, 'Threadname{0}'.format(ins))
            threads.append(thread)
    except Exception as e:
        print e

    # 启动线程
    try:

        for x in range(len(threads)):
            threads[x].start()

        for y in range(len(threads)):
            # ss = time.time()
            # print 'start:{0}'.format(ss)
            threads[y].join()
            # ee = time.time()
            # print 'end:{0}'.format(ee)
            # print 'all_co:{0}'.format(ee - ss)

        for xx in threads:
            all_count += xx.count

    except Exception as e:
        print e


    return all_count

if '__main__' == __name__:
    start_time = time.time()
    content = []

    json_list = []
    total_nums = 40000
    a = int(time.time())
    for ins in range(1, total_nums+1):
        json = {
            "metric": "mutileThreads",
            "timestamp": a,
            "value": math.sin(ins) + 0.9,
            "tags": {
                "name": "zhaolk_11"
            }
        }
        a += 0.5
        json_list.append(json)
        if len(json_list) == 50:
            content.append(json_list)
            json_list = []


    thread_nums = 2

    threadLock = threading.Lock()


    all_count = _run(thread_nums, content)

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

    # print '在{0}秒内，一共访问HTTP Post方法{1}次，Request/Second {2}次/sec，平均响应时间是{3} sec'.format(end_time-start_time, all_count, int(all_count / (end_time-start_time)), sum(res_times)/len(res_times))
    print '{0} thread，Total data {1}，time consuming {2} sec'.format(thread_nums, total_nums, (end_time-start_time)/thread_nums)
    print 'success {0}次 ， failed {1}次'.format(success_nums, failed_nums)


    print '一共执行了{0}'.format(all_count)
