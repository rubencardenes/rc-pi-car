####################################################################
# Ruben Cardenes  --- Feb 2020
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

stickLeft_Horiz  = 0
stickLeft_Vert   = 1
stickRight_Horiz = 2
stickRight_Vert  = 3
axisR2 = 4
axisL2 = 5
sq = 0 # Square button
x  = 1 # X Button
cr = 2 # Circle button
tr = 3 # Triangle button
l1 = 4 # L1 Button
r1 = 5 # L2 Button

max_vz = 50
max_lr = 60

two_axis_control = True
left_axis_control = False
right_axis_control = False

def change_axis_control(a,b,c):
    a, b, c = c, a, b
    return a, b, c

while True:
    connection, client_address = sock.accept()
    R2, L2, StickLR, StickVZ = 0.0, 0.0, 0.0, 0.0
    new_msg = True
    full_msg = b''

    while True:
        # get packets containing controls from PS4
        data = connection.recv(1024)
        if new_msg:
            print("new msg len:", data[:HEADERSIZE])
            try:
                msglen = int(data[:HEADERSIZE])
                new_msg = False
            except:
                msglen = 0
                continue
            #new_msg = False

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

                # Two axis control
                if two_axis_control:
                    event_index_vz = stickLeft_Vert
                    event_index_lr = stickRight_Horiz
                # Only Left axis control
                if left_axis_control:
                    event_index_vz = stickLeft_Vert
                    event_index_lr = stickLeft_Horiz
                # Only Right axis control
                if right_axis_control:
                    event_index_vz = stickRight_Vert
                    event_index_lr = stickRight_Horiz

                if event_index_vz in event['axis']:
                    StickVZ = event['axis'][event_index_vz]
                if event_index_lr in event['axis']:
                    StickLR = event['axis'][event_index_lr]

                # Button data (True or False)
                R1 = event['button'][r1]
                L1 = event['button'][l1]
                X  = event['button'][x]
                SQ = event['button'][sq]
                CR = event['button'][cr]

                if R1:
                    verbose = not verbose
                if L1:
                    two_axis_control, left_axis_control, right_axis_control = change_axis_control(two_axis_control,
                                                                                                  left_axis_control,
                                                                                                  right_axis_control)

                if CR:
                    max_vz += 1
                    max_vz = min(max_vz, 100)
                if SQ:
                    max_lr += 1
                    max_lr = min(max_lr, 100)
                if X:
                    max_lr = 60
                    max_vz = 50

                if verbose:
                    os.system('clear')
                    print(f"R2 {R2}, R1 {R1}, L2 {L2}, L1 {L1}, StickVZ {StickVZ}, StickLR {StickLR}")
                    print("Control modes ", two_axis_control, left_axis_control, right_axis_control)

                dc_vz, dc_lr = 0, 0
                if abs(StickVZ) > 0.1: dc_vz = (abs(StickVZ)) * max_vz
                if abs(StickLR) > 0.1: dc_lr = (abs(StickLR)) * max_lr
                if verbose: print("dc_vz {} dc_lr {}; max_vz {} max_lr {}".format(dc_vz, dc_lr, max_vz, max_lr))


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
