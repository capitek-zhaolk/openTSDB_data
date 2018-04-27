#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
import time
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import requests
import json

import simplejson

def index(request):
    return render(request, 'index.html')

# 处理传入多个时间 生成数据为[['111111', '222222'], ['222222', '333333'], ['333333', '444444']]
def add_lists(*lists):
    new_lists = []
    for only_list in lists:
        new_lists.append(only_list)
    return new_lists


# 处理传入多个时间戳参数 生成数据为['111111', '222222', '333333']
def deal_times(*num_time):
    all_time = []
    new_all_time = []
    new_all_time_copy = []

    # 传入的参数整合为list类型数据
    for ins in num_time:
        all_time += ins

    # 处理整合的时间数据，以正常的形式展示
    for time_list in all_time:
        receive_time = time_list.split('T')
        start_year_mon_day = receive_time[0]
        start_hour_min_sec = receive_time[1]
        start_new_time = '%s %s' % (start_year_mon_day, start_hour_min_sec)
        new_all_time.append(start_new_time)
    new_all_time_copy.append(new_all_time)

    return new_all_time_copy


def get_data_by_post(cond_dic):
    r = requests.post("http://localhost:4242/api/query", json=cond_dic)
    if len(r.json()) > 0:
        dps = r.json()[0]['dps']
        return dps
    else:
        return None

def search(request):
    global result
    global query
    global receive
    global dps
    global dps_receive

    username = request.GET.get('username', '')
    start_time = request.GET.get('start', '')
    end_time = request.GET.get('end', '')


    # print '获取的数据是{0}--{1}--{2}'.format(username, start_time, end_time)

    result = deal_times([start_time], [end_time])
    print 'result是{0}'.format(result)
    time_Array_start = time.strptime(result[0][0], "%Y-%m-%d %H:%M")
    print '开始时间是{0}'.format(time_Array_start)
    timestamps_start = int(time.mktime(time_Array_start))
    time_Array_end = time.strptime(result[0][1], "%Y-%m-%d %H:%M")
    print '结束时间是{0}'.format(time_Array_end)
    timestamps_end = int(time.mktime(time_Array_end))

    # 查询上行数据量
    cond_dic_send = {
        "start": timestamps_start,
        "end": timestamps_end,
        "queries": [
            {
                "aggregator": "sum",
                "metric": "sys.batch.send",
                "tags": {"username": username}
            },
        ]
    }
    # 查询下行流量
    cond_dic_receive = {
        "start": timestamps_start,
        "end": timestamps_end,
        "queries": [
            {
                "aggregator": "sum",
                "metric": "sys.batch.receive",
                "tags": {"username": username}
            },
        ]
    }


    r = requests.post("http://127.0.0.1:4242/api/query?", json=cond_dic_send)
    r_receive = requests.post("http://127.0.0.1:4242/api/query?", json=cond_dic_receive)
    global new_dps_, receive_dps_
    send_receive_dict = {}
    send_list_score = []
    receive_list_score = []
    send_time_list = []
    send_value_list = []
    receive_time_list = []
    receive_value_list = []
    lost_dicts = {}
    lost_lists = []
    if r.status_code == 200 and r_receive.status_code == 200:
        if len(r.json()) > 0:
            dps = r.json()[0]['dps']
            # new_dps = sorted([(v, k) for k, v in dps.items()])
            # new_dps = sorted(dps.items(), key=lambda d:d[0])
            print '发送的数据是{0} 类型是{1}'.format(dps, type(dps))
            new_dps_ = json.dumps(dps)
            send_receive_dict['send'] = new_dps_

        if len(r_receive.json()) > 0:
            receive_dps = r_receive.json()[0]['dps']
            print '接收的数据是{0} 类型是{1}'.format(receive_dps, type(receive_dps))
            receive_dps_ = json.dumps(receive_dps)
            # return HttpResponse(new_dps)
            # return HttpResponse(receive_dps_, content_type='application/json')

            send_receive_dict['receive'] = receive_dps_



        print '最新的字典是{0}'.format(json.dumps(send_receive_dict))
        return HttpResponse(json.dumps(send_receive_dict), content_type='application/json')
