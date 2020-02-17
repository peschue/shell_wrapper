#!/usr/bin/env python3

import logging
import time

import grpc

import oneshot_pb2_grpc as oneshot_grpc
import oneshot_pb2 as oneshot

logging.basicConfig(level=logging.INFO)

def main():
   channel = grpc.insecure_channel('localhost:8080')
   stub = oneshot_grpc.ShellComponentStub(channel)
   request = oneshot.RunRequest()
   stub.Run(request)

main()