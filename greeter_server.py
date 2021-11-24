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
"""The Python implementation of the GRPC helloworld.Greeter server."""
import gc
from concurrent import futures
import logging
import time
import sys

import grpc
import hello_world_pb2
import hello_world_pb2_grpc
from threading import Lock
import traceback
import threading

import cv2
import numpy as np
# import objgraph

from memory_profiler import profile


@profile(precision=4, stream=open(f'{time.time()}.log', 'w+'))
def jpeg_to_np(jpeg):
    try:
        np_str = np.fromstring(jpeg, np.uint8)
        image = cv2.imdecode(np_str, cv2.IMREAD_COLOR)
        del image
        # return image
    except:
        traceback.print_exc()


class Greeter(hello_world_pb2_grpc.GreeterServicer):
    count = 10000

    def SayHello(self, request, context):
        data = request.image.data
        if data:
            # print("make data")
            jpeg_to_np(data)
            # big_array = np.zeros((10000, 4000))
            # print(sys.getsizeof(big_array))

            self.count += 1
            if self.count > 1000:
                self.count = 0
                print(f"thread num: {threading.activeCount()}")
                # roots = objgraph.get_leaking_objects()
                # print('show_most_common_types: ---------------')

                # objgraph.show_most_common_types(objects=roots)
                # print('show_refs: ---------------')
                # objgraph.show_refs(roots[:3], refcounts=True, filename=f'{time.time()}.png')
                #
                # print('show_growth: ---------------')
                # objgraph.show_growth()
                # print('---------------\n\n\n')

                # with open(f'{time.time()}.show', 'w') as f:
                #     print("write data")
                #     f.write(objgraph.show_most_common_types())
        else:
            print('not data')
        return hello_world_pb2.HelloReply(message=f'Hello, {request.name}!')


def serve():
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=100),
        maximum_concurrent_rpcs=2000
    )
    hello_world_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # server.wait_for_termination()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
