#!/bin/bash

cp ../interfaces/shell_wrapper/oneshot.proto oneshot.proto

python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. oneshot.proto
