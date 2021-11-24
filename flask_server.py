#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 7:40 下午
# @Author  : chenDing
import cv2
import numpy as np
# import objgraph
from flask import Flask, request
import threading

app = Flask(__name__)


def jpeg_to_np(jpeg):
    np_str = np.fromstring(jpeg, np.uint8)
    image = cv2.imdecode(np_str, cv2.IMREAD_COLOR)
    return image


@app.route("/", methods=['POST'])
def hello_world():
    files = request.files.get("file")
    # print(files.filename)
    img = jpeg_to_np(files.stream.read())
    print(f"thread num: {threading.activeCount()}")
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(threaded=True)
