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
    def __init__(self, content, theradname, thread_nums):
        threading.Thread.__init__(self, name=theradname)
        self.__running = threading.Event() # 停止多线程的标识
        self.content = content
        self.thread_nums = thread_nums
        self.count = 0
        self.counts = 0

    def sendJson(self, c):
        s = requests.Session()
        start_time_res = time.time()
        r = s.post("http://172.17.0.239:4242/api/put?details", json=c)
        end_time_res = time.time()
        return_list.append(r.text)
        res_times.append(end_time_res - start_time_res)
        # print r.text
        return r.text

    def run(self):
        for ins in xrange(len(self.content)):
            start_ = time.time()
            self.sendJson(self.content[ins])
            # print '线程名称{0}'.format(self.name)
            self.count += 1
            self.counts += 1
            end_ = time.time()

            if self.counts % 100 == 0:
                # print u'每调用Http Post方法{0}次，需耗时{1}秒'.format(100, (end_ - start_)*thread_nums)
                _write('每调用Http Post方法{0}次，需耗时{1}秒'.format(100, (end_ - start_)*thread_nums))
                self.counts = 0
                start_ = end_



        # global threadLock
        #
        # while True:
        #     threadLock.acquire()
        #     length = len(self.content)
        #     if length > 0:
        #         tmp = self.content.pop()
        #         _start = time.time()
        #         self.sendJson(tmp)
        #         self.count += 1
        #         self.counts += 1
        #         _end = time.time()
        #         # print '线程是{0} 数据是{1}'.format(self.name, self.count)
        #         # if self.counts % 100 == 0:
        #         #     print '{0} -- 每调用Http Post接口{1}次， 需耗时{2}'.format(self.name, self.counts, (_end - _start)*100)
        #         #     self.counts = 0
        #         threadLock.release()
        #     else:
        #         threadLock.release()
        #         break

def _run(thread_nums, content):
    threads = []
    all_count = 0
    totalss = 0
    all_time = 1
    _line = 100
    now_time = time.time()

    # 创建线程
    try:
        for ins in range(1, thread_nums + 1):
            thread = ThreadCuts(content, 'Threadname{0}'.format(ins), thread_nums)
            threads.append(thread)
    except Exception as e:
        print e

    # 启动线程
    try:

        for x in range(len(threads)):
            threads[x].start()

        for y in range(len(threads)):
            threads[y].join()

        for xx in threads:
            all_count += xx.count
            totalss += xx.counts

    except Exception as e:
        print e


    return all_count

# print 打屏改换为写入文件
def _write(info):
    fileLog = 'multi_print_info.conf'
    demo = open(fileLog,'a+')
    demo.write(info+'\n')
    demo.close()

def fun_multi(total_nums, thread_nums):
    start_time = time.time()
    content = []
    # json_list批量数据长度
    lists_nums_ = 66
    unit_time = 1 # 单位时间

    json_list = []
    a = int(time.time())
    # a = 1527151531
    for ins in xrange(1, total_nums+1):
        json = {
            "metric": "mutileThreads",
            "timestamp": a,
            "value": math.sin(ins) + 1,
            "tags": {
                "name": "mutile0002"
            }
        }
        a += 0.2
        json_list.append(json)
        if len(json_list) == lists_nums_:
            content.append(json_list)
            json_list = []

    # 剩余的json_list
    content.append(json_list)
    json_list = []

    # threadLock = threading.Lock()

    _write('------------------------------------start-------------------------------------------\n\n\n')

    all_count = _run(thread_nums, content)

    success_nums = 0
    failed_nums = 0

    for xxx in range(len(return_list)):
        resu = return_list[xxx].encode('utf-8')
        for k, v in eval(resu).items():
            if k == 'success':
                success_nums += int(v)
            if k == 'failed':
                failed_nums += int(v)

    end_time = time.time()

    _write('在{0}秒内，一共访问HTTP Post方法{1}次，Request/Second {2}次/秒，平均响应时间为{3}秒'.format(end_time - start_time, all_count, int(all_count / (end_time-start_time)), sum(res_times)/len(res_times)))
    _write('{0} thread，Total data {1}，time consuming {2} sec，每秒可以写入{3}条数据'.format(thread_nums, total_nums, (end_time-start_time)/thread_nums, int(total_nums/((end_time-start_time)/thread_nums))))
    _write('success {0}次 ， failed {1}次'.format(success_nums, failed_nums))

    print u'在{0}秒内，一共访问HTTP Post方法{1}次，Request/Second {2}次/秒，平均响应时间为{3}秒'.format(end_time - start_time, all_count, int(all_count / (end_time-start_time)), sum(res_times)/len(res_times))
    print u'{0} thread，Total data {1}，time consuming {2} sec，每秒可以写入{3}条数据'.format(thread_nums, total_nums, (end_time-start_time)/thread_nums, int(total_nums/((end_time-start_time)/thread_nums)))
    print u'success {0}次 ， failed {1}次'.format(success_nums, failed_nums)

    _write('------------------------------------end-------------------------------------------\n\n\n')



if __name__ == '__main__':

    # 线程数
    thread_nums = 10
    # 数据数量
    total_nums = 100000
    fun_multi(total_nums, thread_nums)





