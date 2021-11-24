# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import cv2
import time

import grpc
import glob
import traceback

from concurrent.futures import ThreadPoolExecutor

import hello_world_pb2
import hello_world_pb2_grpc
from threading import Lock

import uuid
import os


class Count:
    def __init__(self):
        self.count = 0
        self.self_count = 0
        self._lock = Lock()

    def inc(self):
        try:
            self._lock.acquire(timeout=3)
            self.count += 1
            self.self_count += 1
            self._lock.release()
        except:
            traceback.print_exc()
            self._lock.release()

count = Count()
start_time = time.time()


def make_data(filename):
    image = cv2.imread(filename)
    name = str(uuid.uuid4())
    cv2.imwrite(f"{name}.webp", image, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
    with open(f"{name}.webp", 'rb') as f:
        data = f.read()
    os.system(f"rm -rf {name}.webp")
    # 模拟SDK给到的输入图片
    return data


def do_grpc(filename, stub):
    try:

        # print(f'filename:{filename}')
        data = make_data(filename)
        img = hello_world_pb2.Image(
            data=data,
            encoding='webp',
        )
        req = hello_world_pb2.HelloRequest(
            name='say',
            image=img,
        )
        response = stub.SayHello(req)
        # print("Greeter client received: " + response.message)

        count.inc()
        if count.self_count > 1000:
            count.self_count = 0
            print(f"qps is: {count.count/(time.time() - start_time)}")
    except:
        traceback.print_exc()


def run(file_path_list):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    pool = ThreadPoolExecutor(max_workers=20)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_world_pb2_grpc.GreeterStub(channel)
        for file_path, _ in file_path_list:
            res = [pool.submit(do_grpc, filename, stub) for filename in glob.glob(file_path)]
            while not any(res):
                print("等待所有请求结束")
                time.sleep(1)
        pool.shutdown()


if __name__ == '__main__':
    logging.basicConfig()

    file_path_list = [
        ("/Volumes/客户图书/客户资源_old/赶考状元/archive/*/*/*/*.jpg", "gankaozhuangyuan"),
        ("/Volumes/客户图书/Gostudy/phygital/*/*/*.jpg", "phygital"),
        ("/Volumes/客户图书/客户资源/赶考状元/gankaozhuangyuan/更新记录/*/*/*.jpg", "gankaozhuangyuan"),

        ("/Volumes/客户图书/客户资源_old/金龙锋/*/*/*.jpg", "jinlongfeng"),
        ("/Volumes/客户图书/客户资源_old/博尔/algo support/*/*/*.jpg", "boer"),

        ("/Volumes/客户图书/客户资源/博尔/boer/客户原始资源/*/*/*.jpg", "boer"),
        ("/Volumes/客户图书/客户资源/组创/zuchuang/最新资源/*/*.jpg", "zuchuang"),
        ("/Volumes/客户图书/客户资源/highlights/highlights/最新资源/*/*.jpg", "highlights"),
        ("/Volumes/客户图书/客户资源/博尔/boer/客户原始资源/20201130_河北小学英语1起指读图片/*/*.jpg", "boer"),
    ]

    file_path_list_ubuntu_dell1 = [
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源_old/赶考状元/archive/*/*/*/*.jpg",
         "gankaozhuangyuan"),
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/Gostudy/phygital/*/*/*.jpg", "phygital"),
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源/赶考状元/gankaozhuangyuan/更新记录/*/*/*.jpg",
         "gankaozhuangyuan"),

        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源_old/金龙锋/*/*/*.jpg", "jinlongfeng"),
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源_old/博尔/algo support/*/*/*.jpg", "boer"),

        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源/博尔/boer/客户原始资源/*/*/*.jpg", "boer"),
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源/组创/zuchuang/最新资源/*/*.jpg", "zuchuang"),
        ("/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源/highlights/highlights/最新资源/*/*.jpg",
         "highlights"),
        (
        "/run/user/1001/gvfs/smb-share:server=192.168.1.100,share=客户图书/客户资源/博尔/boer/客户原始资源/20201130_河北小学英语1起指读图片/*/*.jpg",
        "boer"),
    ]

    file_path_list_ubuntu_1804 = [
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源_old/赶考状元/archive/*/*/*/*.jpg",
         "gankaozhuangyuan"),
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/Gostudy/phygital/*/*/*.jpg", "phygital"),
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源/赶考状元/gankaozhuangyuan/更新记录/*/*/*.jpg",
         "gankaozhuangyuan"),

        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源_old/金龙锋/*/*/*.jpg", "jinlongfeng"),
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源_old/博尔/algo support/*/*/*.jpg", "boer"),

        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源/博尔/boer/客户原始资源/*/*/*.jpg", "boer"),
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源/组创/zuchuang/最新资源/*/*.jpg", "zuchuang"),
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源/highlights/highlights/最新资源/*/*.jpg",
         "highlights"),
        (
        "/run/user/1000/gvfs/smb-share:server=gostudy.local,share=客户图书/客户资源/博尔/boer/客户原始资源/20201130_河北小学英语1起指读图片/*/*.jpg",
        "boer"),
    ]

    # run(file_path_list)
    run(file_path_list_ubuntu_dell1)
    # run(file_path_list_ubuntu_1804)
