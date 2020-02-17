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

   # we assume the daemon is used with 'clingo' as binary
   request.command_line_parameter.extend(['--models', '6', '--outf=2'])
   request.combine_stdout_stderr = True
   request.obtain_stdout = True
   request.timeout = 10
   request.stdin = b'''1 { a; b; c; d; e } 3. :- a, c. :- b, not e.'''

   response = stub.Run(request)

   logging.info("got response '%s'", response)
   logging.info("stdout was '%s'", response.tool_response.stdout.decode('utf-8'))

main()