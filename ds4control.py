"""Test script for using pygame to read in ds4 controller
with ds4drv  running as a daemon
DS4  controller axis maps:
Axis0: Left stick l-r (-1 left, 1 right)
Axis1: Left stick u-d (-1 up, 1 down)
Axis2: Left trigger (-1 unpressed, 1 completely pressed)
Axis3: Right stick l-r (-1 left, 1 right)
Axis4: Right stick u-d (-1 up, 1 down)
Axis5: Right trigger (-1 unpressed, 1 completely pressed)
"""

import pygame
import wiringpi
from time import sleep
import sys

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#initialise DS4 controller
pygame.joystick.init() #find the joysticks
joy = pygame.joystick.Joystick(0)
joy.init()
controller = joy.get_name() + Connected
print(controller)
  
 while True:
  pygame.event.get()  
  rt = joy.get_axis(5)
  lt = joy.get_axis(2)
  sleep(0.1) #limit the frequency to 10Hz
