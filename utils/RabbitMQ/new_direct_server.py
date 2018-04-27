#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: new_direct_server.py

@time: 2018/3/22/022 18:45

@desc:
'''


import pika
import json
import sys
import time
import os
import requests
import random
import httplib
import socket
import urllib2
import math
from compiler.ast import flatten
import threading
from readfileConfigs import json_list




def send_json(mess):
    r = requests.post("http://localhost:4242/api/put?details", json=mess)
    return r.text

mutex = threading.Lock()
def read_config_lines(index):
    list_dir = '/usr/local/capitek/aaa/data/server/log/radacct/acctrec/'
    new_list = []
    new_ins = []

    username_list = []
    timer_list = []
    value_list = []

    ls = []
    s = requests.Session()


    for ins in index:
        ins = ins.encode('utf-8')
        new_ins = os.path.join(list_dir, ins)
        with open(new_ins, 'r') as files_object:
            contents = files_object.readlines()
            contents_s = contents[1:]
            for ind in range(len(contents_s)):
                new_list.append(contents_s[ind].split('\t'))

    start_time = time.time()

    print '{0}开始传送数据………………'.format(start_time)

    for ins_s in range(len(new_list)):
        timer_s = int(new_list[ins_s][1])
        user_name = str(new_list[ins_s][12])
        value_s = int(new_list[ins_s][14])
        value_r = int(new_list[ins_s][15])

        json_s = {
            "metric": "sys.batch.send",
            "timestamp": timer_s,
            "value": value_s,
            "tags": {
                "username": user_name
            }
        }
        json_r = {
            "metric": "sys.batch.receive",
            "timestamp": timer_s,
            "value": value_r,
            "tags": {
                "username": user_name
            }
        }

        ls.append(json_s)
        ls.append(json_r)
        if len(ls) == 50:
            starts = time.time()
            print '发送中………………'
            send_json(ls)
            time.sleep(0.5)
            ls = []
            ends = time.time()


            print '发送结束………………'
            print '每次发送50条数据，耗时{0}'.format(ends - starts)
        # username_s = str(new_list[ins_s][12])
        # timer_s = int(new_list[ins_s][1])
        # values_s = int(new_list[ins_s][14])
        # values = {
        #     "metric": "user.bytes.send",
        #     "timestamp": timer_s,
        #     "value": values_s,
        #     "tags": {
        #         "username": username_s,
        #     }
        # }
        # ls.append(values)
        # if len(ls) >= 50:
        #     send_json(ls, s)
        #     time.sleep(0.1)
        #     ls = []

    send_json(ls)
    ls = []

    end_time = time.time()
    print '总共发送了{0}条数据'.format(len(new_list))
    print '总共用时{0} 秒'.format((end_time - start_time))


    #     username_list.append(username)
    #     timer_list.append(timer)
    #     value_list.append(values)
    #
    # mess = flatten(zip(timer_list, value_list, username_list))
    # mess_split = [mess[i:i + 3] for i in range(0, len(mess), 3)]

    # start_time = time.time()
    #
    #
    # print '{0}开始传送数据………………'.format(start_time)



    # for ins in range(len(mess_split)):
    #     timestamps = int(mess_split[ins][0])
    #     values_s = int(mess_split[ins][1])
    #     user_name = str(mess_split[ins][2])
    #
    #     values = {
    #         "metric": "user.bytes.send",
    #         "timestamp": timestamps,
    #         "value": values_s,
    #         "tags": {
    #             "username": user_name,
    #         }
    #     }
    #     ls.append(values)
    #     if len(ls) >= 50:
    #         # print '传到数据库的数据是{0}---传到'.format(ls)
    #         send_json(ls, s)
    #         ls = []
    #         time.sleep(0.05)
    #
    # # print '最后传到数据库的数据是{0}--最后'.format(ls)
    # send_json(ls, s)
    # ls = []

    # end_time = time.time()
    # print '总共用时{0} 秒'.format(end_time - start_time)


# def send_open(lists):
#     username_list = []
#     timer_list = []
#     value_list = []
#
#     for inss in range(len(lists)):
#         username = str(lists[inss][12])
#         timer = int(lists[inss][1])
#         values = int(lists[inss][14])
#
#         username_list.append(username)
#         timer_list.append(timer)
#         value_list.append(values)
#
#     mess = flatten(zip(timer_list, value_list, username_list))
#     mess_split = [mess[i:i + 3] for i in range(0, len(mess), 3)]
#
#     send_datas(mess_split)



# def send_datas(mess):
#     start_time = time.time()
#     print '开始传送数据………………'
#
#     ls = []
#     s = requests.Session()
#     # mess = flatten(zip(timer, value, username))
#     # mess_split = [mess[i:i+3] for i in range(0, len(mess), 3)]
#
#     print '数据是{0}长度是{1}'.format(mess, len(mess))
#     for ins in range(len(mess)):
#         timestamps = int(mess[ins][0])
#         values = int(mess[ins][1])
#         usernames = str(mess[ins][2])
#
#         values = {
#             "metric": "user.bytes.send",
#             "timestamp": timestamps,
#             "value": values,
#             "tags": {
#                 "username": usernames,
#             }
#         }
#         ls.append(values)
#         if len(ls) == 50:
#             send_json(ls, s)
#             ls = []
#     send_json(ls, s)
#     ls = []
#
#     end_time = time.time()
#     print '总共用时{0} 秒'.format(end_time - start_time)



def consume():
    try:
        # 创建连接对象
        connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.233'))
        # 创建频道对象
        channel = connection.channel()

        # 指定exchange类型
        channel.exchange_declare(exchange='direct_log_', exchange_type='direct', durable=True)

        # 随机创建一个队列名称
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        severity = 'info'
        # 将该队列与前面创建的exchange做绑定
        # 当绑定完成后,生产者再向 exchange='logs' 中发送消息时,将自动将该消息插入到该队列中
        channel.queue_bind(exchange='direct_log_',
                       queue=queue_name,
                       routing_key=severity
                       )

        print '[***] 开始接受消息!'

        # 取到数据后的回调函数
        def callback(ch, method, properties, body):

            ch.basic_ack(delivery_tag=method.delivery_tag)  # 消息不丢失的关键代码, 对应的是no_ack=False
            body = json.loads(body)
            time.sleep(0.01)
            read_config_lines(body)
            # print "接收的数据是{0} 类型是{1}".format(body, type(body))



        channel.basic_qos(prefetch_count=1)

        # 持续接收 实现高吞吐量
        channel.basic_consume(callback, queue=queue_name, no_ack=False)

        # 开始接收信息，并进入阻塞状态，队列里有消息才回调用callback进行处理
        channel.start_consuming()
    except Exception as e:
        print u'{0} Errors'.format(e)
    finally:
        pass


consume()