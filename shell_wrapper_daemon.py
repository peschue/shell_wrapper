#!/usr/bin/env python3

import logging
import time
from concurrent import futures

import grpc

import oneshot_pb2_grpc as oneshot_grpc
import oneshot_pb2 as oneshot

logging.basicConfig(level=logging.INFO)

class ShellComponent(oneshot_grpc.ShellComponentServicer):
   def Run(self, request, context):
      logging.info("received run request")
      resp = oneshot.RunResponse()
      logging.info("returning response")
      return  resp

def main():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   oneshot_grpc.add_ShellComponentServicer_to_server(ShellComponent(), server)
   server.add_insecure_port('localhost:8080')
   server.start()
   logging.info("serving")
   # not yet in release
   #server.wait_for_termination()
   while True:
      time.sleep(3600)

main()