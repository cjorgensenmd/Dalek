#!/bin/python  
"""Test script for using pygame to read in ds4 controller
with ds4drv  running as a daemon
DS4  controller axis maps:
Axis0: Left stick l-r (-1 left, 1 right)
Axis1: Left stick u-d (-1 up, 1 down)
Axis2: Left trigger (-1 unpressed, 1 completely pressed)
Axis3: Right stick l-r (-1 left, 1 right)
Axis4: Right stick u-d (-1 up, 1 down)
Axis5: Right trigger (-1 unpressed, 1 completely pressed)
"""
import RPi.GPIO as GPIO
import os  
import pygame
import pygame.mixer
from time import sleep
import sys

global DS4


#Start pulseaudio as a daemon
os.system("sudo pulseaudio -D")


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

pygame.mixer.init(48000, -16, 1, 1024)

sndA = pygame.mixer.Sound("note1.wav")
sndB = pygame.mixer.Sound("note2.wav")
sndC = pygame.mixer.Sound("note3.wav")
sndD = pygame.mixer.Sound("note4.wav")
sndE = pygame.mixer.Sound("note5.wav")
sndF = pygame.mixer.Sound("note6.wav")
sndG = pygame.mixer.Sound("note7.wav")
sndH = pygame.mixer.Sound("note8.wav")

soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)
soundChannelC = pygame.mixer.Channel(3)
soundChannelD = pygame.mixer.Channel(4)
soundChannelE = pygame.mixer.Channel(5)
soundChannelF = pygame.mixer.Channel(6)
soundChannelF = pygame.mixer.Channel(7)
soundChannelF = pygame.mixer.Channel(8)
print ("Soundboard loaded")
os.system("espeak -p 1 -v english-us 'Soundboard loaded'")



def Dualshock4Init():
    global DS4
    # Setup pygame and wait for the joystick to become available
    pygame.init()
    # Set the width and height of the screen [width,height]
    size = [500, 700]
    screen = pygame.display.set_mode(size)
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Get ready to print
    textPrint = TextPrint()
    pygame.display.set_caption("Dalek Control")
    print ('Waiting for joystick... (press CTRL+C to abort)')
    os.system("espeak -p 1 -v english-us 'Waiting for joystick.....'")

    while True:
        try:
            try:
                pygame.joystick.init()
                # Attempt to setup the joystick
                if pygame.joystick.get_count() < 1:
                    # No joystick attached
                    pygame.joystick.quit()
                    time.sleep(0.1)
                else:
                    # We have a joystick, attempt to initialise it!
                    DS4 = pygame.joystick.Joystick(0)
                    os.system("espeak -p 1 -v english-us 'Joystick Connected!'")
                    break
            except pygame.error:
                # Failed to connect to the joystick
                pygame.joystick.quit()
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C exit, give up
            print ('\nUser aborted')
            sys.exit()
    print ('Joystick found')
    DS4.init()
    


def DalekControl():
    global DS4
    try:
        print ('Press CTRL+C to quit')
        os.system("espeak -p 1 -v english-us 'Press CTRL+C to quit'")
       # driveLeft = 0.0
        #driveRight = 0.0
        running = True
        hadEvent = False
       # upDown = 0.0
        #leftRight = 0.0
        # Loop indefinitely
        while running:
            # Get the latest events from the system
            hadEvent = False
            events = pygame.event.get()
            # DRAWING STEP
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            screen.fill(WHITE)
            textPrint.reset()

            # Get name of controller
            name = DS4.get_name() 

            textPrint.print(screen, "{}".format(name) )
            textPrint.indent()
    
            # Handle each event individually
            for event in events:
                print("event:{}".format(event.type))
                if event.type == pygame.QUIT:
                    # User exit
                    running = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    # A button on the joystick just got pushed down
                    hadEvent = True
                elif event.type == pygame.JOYAXISMOTION:
                    # A joystick has been moved
                    hadEvent = True
                elif event.type == pygame.JOYHATMOTION:
                    # A D-pad button has been moved
                    hadEvent = True
                if hadEvent: #assigning buttons 
                    LSLR = DS4.get_axis(0) #Left stick left right (-1 left, 1 right)
                    LSUD = DS4.get_axis(1) #Left stick up down (-1 up, 1 down)
                    RSLR = DS4.get_axis(3) #Right stick left right (-1 left, 1 right)
                    RSUD = DS4.get_axis(4) #Left stick up down (-1 up, 1 down)
                    R2 = DS4.get_axis(5) # R2 (-1 unpressed, 1 completely pressed)
                    L2 = DS4.get_axis(2) # L2 (-1 unpressed, 1 completely pressed)
                    Triangle =DS4.get_button(0)
                    Circle = DS4.get_button(0)
                    Square = DS4.get_button(0)
                    X = DS4.get_button(0)
                    L1 = DS4.get_button(0)
                    R1 = DS4.get_button(0)
                    L3 = DS4.get_button(0)
                    R3 = DS4.get_button(0)
                    PS = DS4.get_button(0)
                    Share = DS4.get_button(0)
                    Options = DS4.get_button(0)
                    #Dpad1 = DS4.get_hat(0)
                    #Dpad2 =  DS4.get_hat(0)

                        #Code for soundboard
                    if Triangle and not soundChannelA.get_busy(): #checks to see if button is pressed and sound is already playing or not
                        soundChannelA.play(sndA)
                        textPrint.print(screen, "Playing sndA!")
                    elif Triangle and soundChannelA.get_busy(): #if sound is playing, then dont play sound
                        textPrint.print(screen, "Waiting for sndA to finish!")
                    if Circle and not soundChannelB.get_busy():
                        soundChannelB.play(sndB)
                        textPrint.print(screen, "Playing sndB!")
                    elif Circle and soundChannelB.get_busy():
                        textPrint.print(screen, "Waiting for sndB to finish!")
                    if Square and not soundChannelC.get_busy():
                        soundChannelC.play(sndC)
                        textPrint.print(screen, "Playing sndC!")
                    elif Square and soundChannelC.get_busy():
                        textPrint.print(screen, "Waiting for sndC to finish!")
                    if X and not soundChannelD.get_busy():
                        soundChannelD.play(sndD)
                        textPrint.print(screen, "Playing sndD!")
                    elif X and soundChannelD.get_busy():
                        textPrint.print(screen, "Waiting for sndD to finish!")
                else:
                    sleep(0.1) #limit the frequency to 10Hz              
    except KeyboardInterrupt:
        # CTRL+C exit, disable all drives
        os.system("espeak -p 1 -v english-us 'Exiting program'")

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
