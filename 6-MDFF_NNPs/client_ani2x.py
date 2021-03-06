#!/usr/bin/env python3
import socket
import os
import sys
import time

sock_address = os.environ['SLURM_TMPDIR'] + '/ani_socket'

if(os.path.exists(sys.argv[1] + '.result')):
   os.system('rm ' + sys.argv[1] + '.result')

if os.path.exists(sock_address):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(sock_address)
    client.send(sys.argv[1].encode('utf-8'))
    client.recv(1)
                       

