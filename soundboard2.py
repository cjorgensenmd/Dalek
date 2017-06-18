"""Test script for using pygame to read in ds4 controller
with ds4drv  running as a daemon
DS4  controller axis maps:
X 1
Square 0
O 2
Triangle 3
R1 5
L1 4
R2 7 and axis 4
L2 axis 3 and button 6
R stick button 11
L stick button 10
Options 9
Share 8
D pad hat
Click 13
PS 12
L stick L/R axis 0 (L -1 R 1)
L stick up/down axis 1 (up -1 down 1)
R stick L/R axis 2 (L -1 R 1)
R stick up/down axis 5 (up -1 down 1)
"""

import os  
import pygame
import pygame.mixer
from time import sleep
import sys


pygame.mixer.init(48000, -16, 1, 1024)

sndA = pygame.mixer.Sound("Obey.wav")
sndB = pygame.mixer.Sound("youwillbeexterminated!.wav")
sndC = pygame.mixer.Sound("annihilate.wav")
sndD = pygame.mixer.Sound("Emrgncy.wav")
sndE = pygame.mixer.Sound("R2D2.wav")
sndF = pygame.mixer.Sound("Tardis.wav")
sndG = pygame.mixer.Sound("Theme.wav")
sndH = pygame.mixer.Sound("Intruder.wav")

soundChannelA = pygame.mixer.Channel(0)
soundChannelB = pygame.mixer.Channel(1)
soundChannelC = pygame.mixer.Channel(2)
soundChannelD = pygame.mixer.Channel(3)
soundChannelE = pygame.mixer.Channel(4)
soundChannelF = pygame.mixer.Channel(5)
soundChannelF = pygame.mixer.Channel(6)
soundChannelF = pygame.mixer.Channel(7)
print ("Soundboard loaded")

#os.system("espeak -p 1 -v english-us 'Soundboard loaded'")

global DS4 #create global variable

def Dualshock4Init():
    global DS4
    # Setup pygame and wait for the joystick to become available
    pygame.init()
    print 'Waiting for joystick... (press CTRL+C to abort)'
    while True:
        try:
            try:
                pygame.joystick.init()
                # Attempt to setup the joystick
                if pygame.joystick.get_count() < 1:
                    Print("No joystick attached")
                    pygame.joystick.quit()
                    sleep(0.1)
                else:
                    # We have a joystick, attempt to initialise it!
                    DS4 = pygame.joystick.Joystick(0)
                    break
            except pygame.error:
                print("Failed to connect to the joystick")
                pygame.joystick.quit()
                sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C exit, give up
            print '\nUser aborted'
            sys.exit()
    print 'Joystick found'
    DS4.init()
    

def soundboard():
    global DS4
    print ('Press CTRL+C to quit')
    if not DS4.get_init():
        print("re-initializing controller")
        DS4.init()
    elif DS4.get_init():
        print("DS4 Initialized")
    else:
        print("WTF?")
    while True:
        try:
            pygame.event.get()
            LSLR = DS4.get_axis(0) #Left stick left right (-1 left, 1 right)
            LSUD = DS4.get_axis(1) #Left stick up down (-1 up, 1 down)
            RSLR = DS4.get_axis(2) #Right stick left right (-1 left, 1 right)
            RSUD = DS4.get_axis(5) #Left stick up down (-1 up, 1 down)
            R2 = DS4.get_axis(4) # R2 (-1 unpressed, 1 completely pressed)
            L2 = DS4.get_axis(3) # L2 (-1 unpressed, 1 completely pressed)
            Triangle =DS4.get_button(3)
            Circle = DS4.get_button(2)
            Square = DS4.get_button(0)
            X = DS4.get_button(1)
            L1 = DS4.get_button(4)
            R1 = DS4.get_button(5)
            L3 = DS4.get_button(10) #button under L stick
            R3 = DS4.get_button(11) #button under R stick
            PS = DS4.get_button(12)
            Share = DS4.get_button(8)
            Options = DS4.get_button(9)
            #Dpad1 = DS4.get_hat(0)
            #Dpad2 =  DS4.get_hat(0)
            #Code for soundboard
            if Triangle and not pygame.mixer.get_busy(): #checks to see if button is pressed and sound is already playing or not
                soundChannelA.play(sndA)
                print("Playing sndA!")
            elif Triangle and pygame.mixer.get_busy(): #if sound is playing, then dont play sound
                print("Waiting for sndA to finish!")
            if Circle and not pygame.mixer.get_busy():
                soundChannelB.play(sndB)
                print("Playing sndB!")
            elif Circle and pygame.mixer.get_busy():
                print("Waiting for sndB to finish!")
            if Square and not pygame.mixer.get_busy():
                soundChannelC.play(sndC)
                print("Playing sndC!")
            elif Square and pygame.mixer.get_busy():
                print("Waiting for sndC to finish!")
            if X and not pygame.mixer.get_busy():
                soundChannelD.play(sndD)
                print("Playing sndD!")
            elif X and pygame.mixer.get_busy():
                print("Waiting for sndD to finish!")
            sleep(0.1) #limit the frequency to 10Hz              
        except KeyboardInterrupt:
            print("Stopping...")
            pygame.quit()

Dualshock4Init()
soundboard()
        
