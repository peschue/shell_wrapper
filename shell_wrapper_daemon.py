#!/usr/bin/env python3

import logging
import time
import tempfile
import os
import os.path
import subprocess
import traceback
from concurrent import futures

import grpc

import oneshot_pb2_grpc as oneshot_grpc
import oneshot_pb2 as oneshot

BINARY = '/home/staff/ps/.local/bin/clingo'
#LOGLEVEL = logging.INFO
LOGLEVEL = logging.WARNING

logging.basicConfig(level=LOGLEVEL)

class ShellComponent(oneshot_grpc.ShellComponentServicer):
   def __init__(self, binary):
      # binary is the binary to execute with Run()
      self.binary = binary

   def _create_input_files(self, filebase, input_files):
      logging.info("creating input files")
      for fileid, filespec in input_files.items():
         if any([ p in ['.', '..', '*'] for p in filespec.location.path ]):
            raise Exception('input files cannot use ., .., * in path, got %s', filespec.path)
         fullpath = os.path.join(filebase, filespec.location.path)
         os.makedirs(fullpath, exist_ok=True)
         with open(os.path.join(fullpath, filespec.location.filename), 'w+b') as outf:
            outf.write(filespec.content)

   def Run(self, request, context):
      logging.info("received run request")

      # TODO implement request.output_files and resp.tool_response.output_files
      if len(request.output_files) > 0:
         raise Exception("output_files is currently not implemented!")

      try:
         # creates temporary directory, removes it and contents afterwards
         with tempfile.TemporaryDirectory() as tempcwd:
            logging.info("running in temp directory %s", tempcwd)

            filebase = os.path.join(tempcwd , 'files')
            os.mkdir(filebase)
            self._create_input_files(filebase, request.input_files)

            stdin = subprocess.PIPE if request.stdin else None
            stdout = subprocess.PIPE if request.obtain_stdout else None
            stderr = subprocess.PIPE if request.obtain_stderr else None
            if request.combine_stdout_stderr:
               stderr = subprocess.STDOUT
               if not request.obtain_stdout:
                  raise Exception("if combine_stdout_stderr then we require obtain_stdout")
               if request.obtain_stderr:
                  raise Exception("if combine_stdout_stderr then we cannot have obtain_stderr")

            logging.info("starting %s", self.binary)
            child = subprocess.Popen(
               cwd = tempcwd,
               executable = self.binary,
               args = request.command_line_parameter,
               stdin = stdin,
               stdout = stdout,
               stderr = stderr,
               text = False, encoding = None) # these are important!

            logging.info("communicating with timeout %d", request.timeout)
            try:
               stdout_data, stderr_data = child.communicate(input=request.stdin, timeout=request.timeout)
            except subprocess.TimeoutExpired:
               logging.warning("killing after timeout!")
               child.kill()
               stdout_data, stderr_data = child.communicate()

            logging.info("got return code %d", child.returncode)
            logging.info("got stdout %s", stdout_data)
            logging.info("got stderr %s", stderr_data)

            resp = oneshot.RunResponse()
            resp.success = True
            resp.tool_response.exitcode = child.returncode
            if stdout_data:
               resp.tool_response.stdout = stdout_data
            if stderr_data:
               resp.tool_response.stderr = stderr_data
            # TODO implement request.output_files and resp.tool_response.output_files
            logging.info("returning response")
            return resp

      except Exception:
         logging.warning("got exception %s", traceback.format_exc())
         resp = oneshot.RunResponse()
         resp.success = False
         resp.request_error = traceback.format_exc()
         return resp

def main():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   oneshot_grpc.add_ShellComponentServicer_to_server(ShellComponent(BINARY), server)
   server.add_insecure_port('localhost:8080')
   server.start()
   logging.info("serving")
   # not yet in release
   #server.wait_for_termination()
   while True:
      time.sleep(3600)

main()