#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: Multi_thread.py

@time: 2018/4/26/026 14:41

@desc:
'''

# 多线程

import time
import math
import requests
import json
import threading

threadLock = threading.Lock()
num = 0
class timer(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self)
        # self.interval = interval
        self.count = count

    def run(self):
        global num
        while True:
            # 获得锁
            threadLock.acquire()
            if num >= self.count:
                # 释放锁
                threadLock.release()
                break
            num += 1
            print 'Thread name:%s, %d' % (main(), num)
            # main()
            # 释放锁
            threadLock.release()

            time.sleep(0.5)

def send_json(jsons, s):
    r = s.post("http://172.17.0.239:4242/api/put?details", json=jsons)
    return r.text

def main():
    s = requests.Session()
    a = int(time.time())
    json = {
        "metric": "sys.batch.duoxiancheng",
        "timestamp": a,
        "value": int(2456789),
        "tags": {
            "name": "zhaolk_servers"
        }
    }
    t = send_json(json, s)
    print '数据是{0}'.format(t)
if __name__ == "__main__":
    total_nums = 1000
    print_nums = 20
    st1 = 0
    end1 = 0
    threads = []
    start_time = time.time()
    for i in range(print_nums):
        myThread = timer(total_nums)
        # myThread.start()
        threads.append(myThread)

    for y in range(print_nums):
        st1 = time.time()
        threads[y].start()

    for ins in range(print_nums):
        threads[ins].join()
        end1 = time.time()

    end_time = time.time()

    print '{0}条数据分{1}个线程, 总共耗时{2}/ sec ,每个线程包含{3}条数据'.format(
        total_nums,
        total_nums/print_nums,
        (end_time - start_time)/1000,
        total_nums/(total_nums/print_nums)
    )

