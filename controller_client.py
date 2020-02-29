####################################################################
# Ruben Cardenes, Clay L. McLeod  -- Feb 2019
#
# File:        controller_client.py
#
# Description: This script has to be executed on the computer connected to a
#              Playstation 4 Controller by USB. No driver installation needed,
#              simply plug your PS4 controller into your computer using USB
#              This script was modified to send packets to another device (like
#              Raspberry PI) accepting the PS4 controls to do something
#
# NOTE: We assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# NOTE: Tested on Linux and MacOS
#
# This is a modification from a script by Clay L. McLeod <clay.l.mcleod@gmail.com>
# Distributed under terms of the MIT license.
####################################################################


import os
import pprint
import pygame
import socket
import pickle
import sys
from threading import Thread

HEADERSIZE = 10

class PS4Controller(object):
    """Class representing the PS4 controller"""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self, address, port):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.event_dict = {}

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (address, port)
        print('connecting to {} port {}'.format(address, port))
        self.sock.connect(server_address)

        self.verbose = True

    def listen_and_send(self):
        """Listen for events to happen and send commands"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                if event.type == pygame.JOYBUTTONDOWN:
                    # A button on the joystick just got pushed down
                    hadEvent = True
                elif event.type == pygame.JOYAXISMOTION:
                    # A joystick has been moved
                    hadEvent = True

                if hadEvent:

                    self.event_dict['axis'] = self.axis_data
                    self.event_dict['button'] = self.button_data
                    message = pickle.dumps(self.event_dict, protocol=4)
                    message = bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message
                    self.sock.sendall(message)

                    if self.button_data[4]:
                        self.verbose = not self.verbose

                    if self.verbose:
                        os.system('clear')
                        print("Button ")
                        pprint.pprint(self.button_data)
                        print("Axis ")
                        pprint.pprint(self.axis_data)
                        # print("Motion ")
                        # pprint.pprint(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    server_hostname = 'localhost'
    if len(sys.argv) > 1:
        server_hostname = sys.argv[1]
    print("Starting connection to ", server_hostname)
    ps4.init(server_hostname, 10200)
    t = Thread(target=ps4.listen_and_send(), args=()).start()
    # Non-threaded version
    # ps4.listen_and_send()
