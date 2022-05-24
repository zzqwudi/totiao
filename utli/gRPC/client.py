# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wenjie
@file: client.py
@time: 2022/5/23 11:29
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

import grpc

from utli.gRPC.base_package import data_pb2, data_pb2_grpc

_HOST = 'localhost'
_PORT = '9955'


def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)  # 监听频道
    client = data_pb2_grpc.FormatDataStub(
        channel=conn)  # 客户端使用Stub类发送请求,参数为频道,为了绑定链接
    response = client.DoFormat(
        data_pb2.actionrequest(text='apple!'))  # 返回的结果就是proto中定义的类
    print(response)
    print("received: " + response.text)


if __name__ == '__main__':
    run()
