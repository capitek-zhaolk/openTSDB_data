#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@author: zhaolk

@license: (C) Copyright capitek

@contact: zhaolk@capitek.com.cn

@Software : PyCharm

@file: new_direct_client.py

@time: 2018/3/22/022 18:41

@desc:
'''

import pika
import json
import sys
import time

def timeSleep(hours, mins, secs):
    return hours * 3600 + mins * 60 + secs

seconds = timeSleep(0, 0, 5)


def rabbitMQClient():
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.233'))
    try:
        channel = connection.channel()

        # 指定exchange='logs'
        channel.exchange_declare(exchange='direct_logs_', exchange_type='direct', durable=True)

        severitys = ['info', 'waring', 'error']

        message = 'Hello World Man'

        for severity in severitys:
            channel.basic_publish(exchange='direct_logs_',
                                  routing_key=severity,
                                  body=message,
                                  properties=pika.BasicProperties(delivery_mode=2, )
                                  )
        print u"发送的数据是{0} 类型是{1} 长度是{2}".format(message, type(message), len(message))

    except Exception as e:
        print u'{0} Errors'.format(e)
    finally:
        connection.close()

while True:
    time.sleep(seconds)
    rabbitMQClient()