####################################################################
# Ruben Cardenes -- Feb 2020
#
# File:        controller_server_on_pi.py
# Description: This program runs in a Raspberry PI and uses the PS4 controller to
#              output signal and control a remote control car
#              Left stick controls the car acceleration
#              Right stick controls the car steering
#
# Initial version downloaded from: http://www.elektronx.de/motoren-mit-ps4-controller-steuern/
####################################################################

import socket
import pickle
import sys
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

IN1 = 11
IN2 = 13
IN3 = 16
IN4 = 18
ENA = 32
ENB = 33

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

ENA_PWM = GPIO.PWM(ENA, 100)
ENB_PWM = GPIO.PWM(ENB, 100)

ENA_PWM.start(0)
ENB_PWM.start(0)

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

two_axis_control = False
left_axis_control = True
right_axis_control = False

os.system("node /home/pi/PycharmProjects/h264-live-player-master/server-rpi.js &")

verbose = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('0.0.0.0', 10200)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

HEADERSIZE = 10

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
            try:
                msglen = int(data[:HEADERSIZE])
                new_msg = False
            except:
                new_msg = True
                continue

        full_msg += data

        # If message is fully received, load the packet as a pickle object
        if len(full_msg) - HEADERSIZE >= msglen:
            # print("full msg recvd")
            event = pickle.loads(full_msg[HEADERSIZE:])
            # We set the new_msg flag to True
            new_msg = True
            # and reset the full message empty
            full_msg = b""

            # event is just a dictionary with two entries: 'axis' and 'button'
            # If event is found, then we just need to get those entries
            if event is not None:
                # Axis data (float values)
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

                # if R1 is received, we turn verbose mode on or off
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
                    os.system('clear') # this system call can make the reception a bit slow
                    # Printing some of the received command values
                    print(f"R2 {R2}, R1 {R1}, L2 {L2}, L1 {L1}, StickVZ {StickVZ}, StickLR {StickLR}")
                    print("Control modes ", two_axis_control, left_axis_control, right_axis_control)

                dc_vz, dc_lr = 0, 0
                if abs(StickVZ) > 0.1: dc_vz = (abs(StickVZ)) * max_vz
                if abs(StickLR) > 0.1: dc_lr = (abs(StickLR)) * max_lr
                if verbose: print("dc_vz {} dc_lr {}; max_vz {} max_lr {}".format(dc_vz, dc_lr, max_vz, max_lr))
                ENA_PWM.ChangeDutyCycle(dc_vz) # Motor speed control for rear wheels
                ENB_PWM.ChangeDutyCycle(dc_lr) # Motor speed control for direction wheels

                # Now the logic to send the right command to the GPIO PINs
                if StickLR < -0.1:
                    if verbose: print("--- Left")
                    GPIO.output(IN3, False)
                    GPIO.output(IN4, True)

                if StickLR > 0.1:
                    if verbose: print("--- Right")
                    GPIO.output(IN3, True)
                    GPIO.output(IN4, False)

                if abs(StickLR) <= 0.1:
                    if verbose: print("--- No LR")
                    GPIO.output(IN3, False)
                    GPIO.output(IN4, False)

                if StickVZ > 0.2:
                    if verbose: print("--- Backwards")
                    GPIO.output(IN1, False)
                    GPIO.output(IN2, True)

                if StickVZ < - 0.2:
                    if verbose: print("--- Forward ")
                    GPIO.output(IN1, True)
                    GPIO.output(IN2, False)

                if abs(StickVZ) < 0.2:
                    if verbose: print("--- No move")
                    GPIO.output(IN1, False)
                    GPIO.output(IN2, False)

    connection.close()
