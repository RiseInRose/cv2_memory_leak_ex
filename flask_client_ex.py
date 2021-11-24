#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 7:40 下午
# @Author  : chenDing
import requests
import logging
import cv2
import time

import grpc
import glob
import traceback
import json

from concurrent.futures import ThreadPoolExecutor

import uuid
import os
from threading import Lock


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


def make_data(filename):
    image = cv2.imread(filename)
    name = str(uuid.uuid4())
    cv2.imwrite(f"{name}.webp", image, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
    with open(f"{name}.webp", 'rb') as f:
        data = f.read()
    os.system(f"rm -rf {name}.webp")
    # 模拟SDK给到的输入图片
    return data


def do_request(filename, start_time):
    try:
        # print(f'filename:{filename}')
        data = make_data(filename)
        response = requests.post(url="http://127.0.0.1:5000", files={"file": data})
        # print("Greeter client received: " + response.content.decode())
        count.inc()
        if count.self_count > 1000:
            count.self_count = 0
            print(f"qps is: {count.count/(time.time() - start_time)}")
    except:
        traceback.print_exc()


def run(file_path_list):
    start_time = time.time()
    pool = ThreadPoolExecutor(max_workers=10)
    for file_path, _ in file_path_list:
        res = [pool.submit(do_request, filename, start_time) for filename in glob.glob(file_path)]
        while not any(res):
            print("等待所有请求结束")
            time.sleep(1)
    pool.shutdown()

    # do_request('/Users/caturbhuja/goStudy/svc_DevOps/grpc_test/test/source/git的副本.jpeg')


if __name__ == '__main__':
    logging.basicConfig()
    count = Count()

    file_path_list = [
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=highlights/*/*.jpg",
         "highlights"),
        (
            "/run/user/1000/gvfs/smb-share:server=gostudy.local,share=20201130/*/*.jpg",
            "boer"),
    ]

    file_path_list_ubuntu_dell1 = [
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=highlights/*/*.jpg",
         "highlights"),
        (
            "/run/user/1000/gvfs/smb-share:server=gostudy.local,share=20201130/*/*.jpg",
            "boer"),
    ]

    file_path_list_ubuntu_1804 = [
        ("/run/user/1000/gvfs/smb-share:server=gostudy.local,share=highlights/*/*.jpg",
         "highlights"),
        (
            "/run/user/1000/gvfs/smb-share:server=gostudy.local,share=20201130/*/*.jpg",
            "boer"),
    ]

    # run(file_path_list)
    run(file_path_list_ubuntu_dell1)
    # run(file_path_list_ubuntu_1804)

