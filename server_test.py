####################################################################
# Ruben Cardenes  --- Feb 2019
#
# File:        Server_test.py
# Description: This script starts a socket that listens to
#              incoming packets containing PS4 controller commands. It does nothing useful,
#              it is only for testing your PS4 controller works properly
#              Run this script on your local machine:
#              $ python3 server_test.py
#              and then run controller_client.py
#              $ python3 controller_client.py localhost
####################################################################

import os
import socket
import sys
import pickle

verbose = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10200)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
HEADERSIZE = 10

axisR2 = 4
axisL2 = 5
stickVZ = 1
if sys.platform == "linux":
    stickLR = 3
if sys.platform == "darwin":
    stickLR = 2

r1 = 4
l1 = 5

while True:
    connection, client_address = sock.accept()
    R2, L2, StickLR, StickVZ = 0.0, 0.0, 0.0, 0.0
    new_msg = True
    full_msg = b''

    while True:
        data = connection.recv(512)
        if new_msg:
            print("new msg len:", data[:HEADERSIZE])
            try:
                msglen = int(data[:HEADERSIZE])
            except:
                msglen = 0
            new_msg = False

        print(f"full message length on header: {msglen}")

        full_msg += data

        print(f"message length real {len(full_msg)}")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            event = pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b''

            if event is not None:
                if axisR2 in event['axis']:
                    R2 = event['axis'][axisR2]
                if axisL2 in event['axis']:
                    L2 = event['axis'][axisL2]

                R1 = event['button'][r1]
                L1 = event['button'][l1]

                if stickVZ in event['axis']:
                    StickVZ = event['axis'][stickVZ]
                if stickLR in event['axis']:
                    StickLR = event['axis'][stickLR]

                if R1:
                    verbose = not verbose

                if verbose:
                    os.system('clear')
                    print(f"R2 {R2}, R1 {R1}, L2 {L2}, L1 {L1}, StickVZ {StickVZ}, StickLR {StickLR}")

                dc_vz, dc_lr = 0, 0
                if abs(StickVZ) > 0.1: dc_vz = (abs(StickVZ)) * 20
                if abs(StickLR) > 0.1: dc_lr = (abs(StickLR)) * 20


                if StickLR < -0.1:
                    if verbose: print("--- Left")

                if StickLR > 0.1:
                    if verbose: print("--- Right")

                if abs(StickLR) <= 0.1:
                    if verbose: print("--- No LR")

                if StickVZ > 0.2:
                    if verbose: print("--- Backwards")

                if StickVZ < - 0.2:
                    if verbose: print("--- Forward ")

                if abs(StickVZ) < 0.2:
                    if verbose: print("--- No move")


    connection.close()
