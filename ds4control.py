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

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10


pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Get ready to print
textPrint = TextPrint()

#initialise DS4 controller
pygame.joystick.init() #find the joysticks
joy = pygame.joystick.Joystick(0)

while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()


    
joy.init()
controller = joy.get_name() + Connected
print(controller)
  
 while True:
  pygame.event.get()  
  rt = joy.get_axis(5)
  lt = joy.get_axis(2)
  sleep(0.1) #limit the frequency to 10Hz
