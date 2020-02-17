#!/bin/bash

GRPC_ENABLE_FORK_SUPPORT=0 \
python3 shell_wrapper_daemon.py &
DPID=$!

sleep 1

python3 shell_wrapper_testclient.py

kill $DPID

