import os  
import pygame
import pygame.mixer
from time import sleep
import sys
import RPi.GPIO as GPIO
import serial

#setting up GPIO in broadcom mode, using pin 21 as output
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#set up serial connection
ser = serial.Serial("/dev/rfcomm0", baudrate=9600)
global serialstring
serialstring = '<0,0,0,0,0,0,0>'

#setting up counter for press down events
global count
count = 0

global count1
count1 = 0

global count2
count1 = 0

#set up drive states
global parked
global driving
global brakes
brakes = True
parked = True
driving = False


#setup pygame mixer and soundboard
pygame.init()
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
soundChannelG = pygame.mixer.Channel(6)
soundChannelH = pygame.mixer.Channel(7)
print ("Soundboard loaded")

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
    
def motors():
    global DS4
    global serialstring
    global count
    global count1
    global count2
    global parked
    global driving
    global brakes
    print ('Press CTRL+C to quit')
    M1 = GPIO.PWM(13, 100) #Motor 1 output pin 5 PWM mode at 100Hz
    M2 = GPIO.PWM(26, 100) #Motor 2 output pin 13 PWM mode at 100Hz
    Dir1 = 0
    Dir2 = 0
    GPIO.output(6,0) #initializes direction for motor 1
    GPIO.output(19,0) #initializes direction for motor 2
    M1.start(0)
    M2.start(0)
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
            Dpad = DS4.get_hat(0)
            
            
            # code for Dome Motors
            RSLR = int(RSLR*99)
            RSLRamp = abs(RSLR)
            RSUD = int(RSUD*99)
            RSUDamp = abs(RSUD)
            if RSLR>=0:
                GPIO.output(6,1)
                Dir1 = 1
            else:
                GPIO.output(6,0)
                Dir1 = 0
            M1.ChangeDutyCycle(RSLRamp)
            
            if RSUD>=0:
                GPIO.output(19,1)
                Dir2 = 1
            else:
                GPIO.output(19,0)
                Dir2 = 0
            M2.ChangeDutyCycle(RSUDamp)

            #PS button
            if PS and count>=20:
                if parked and not driving:
                    driving = True
                    parked = False
                    print("Driving mode Activated!")
                    count = 0
                elif driving and not parked:
                    driving = False
                    parked = True
                    print("Parking mode Activated!")
                    count = 0
                else:
                    driving = False                    
                    parked = True
                    count = 0
            elif PS and count<=19:
                count = int(count+1)
            else:
                count = 0
                
            #wheelchair motors
            speed = int((L2+1)*50) 
            if parked:
                brakes = True
            elif driving and not PS:
                brakes = False
            
            elif driving and PS:
                brakes = True
                

            #front eye
            if count1<99:
                eye = int(count1*2.5)
                count1 = count1+1
            elif count1>=99 and count1<200:
                eye = int(350-count1)
                count1 = count1+1
            elif count1>=200:
                if Dpad == (-1,1) or Dpad == (0,1) or Dpad == (1,1) and eye<=250:
                    eye = eye +5
                elif Dpad == (-1,-1) or Dpad == (0,-1) or Dpad == (1,-1) and eye>=5:
                    eye = eye-5
                elif eye>=255:
                    eye = 255
                elif eye<0:
                    eye = 0

            #Ears
            if R1:
                ear=int(255)
            else:
                ear = int(0)
                

            

            #Code for soundboard
            if Triangle and L1 and not pygame.mixer.get_busy(): #checks to see if button is pressed and sound is already playing or not
                soundChannelE.play(sndE)
                print("Playing sndE!")
            elif Triangle and pygame.mixer.get_busy(): #if sound is playing, then dont play sound
                print("Waiting for other sound to finish!")
            if Circle and L1 and not pygame.mixer.get_busy():
                soundChannelF.play(sndF)
                print("Playing sndF!")
            elif Circle and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")
            if Square and L1 and not pygame.mixer.get_busy():
                soundChannelG.play(sndG)
                print("Playing sndG!")
            elif Square and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")
            if X and L1 and not pygame.mixer.get_busy():
                soundChannelH.play(sndH)
                print("Playing sndH!")
            elif X and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")
                
            if Triangle and not pygame.mixer.get_busy(): #checks to see if button is pressed and sound is already playing or not
                soundChannelA.play(sndA)
                print("Playing sndA!")
            elif Triangle and pygame.mixer.get_busy(): #if sound is playing, then dont play sound
                print("Waiting for other sound to finish!")
            if Circle and not pygame.mixer.get_busy():
                soundChannelB.play(sndB)
                print("Playing sndB!")
            elif Circle and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")
            if Square and not pygame.mixer.get_busy():
                soundChannelC.play(sndC)
                print("Playing sndC!")
            elif Square and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")
            if X and not pygame.mixer.get_busy():
                soundChannelD.play(sndD)
                print("Playing sndD!")
            elif X and pygame.mixer.get_busy():
                print("Waiting for other sound to finish!")


            
            servo = 0
            
            M1arduino = int(RSLRamp*2.5)
            M2arduino = int(RSUDamp)

            serialstring = '<%d,%d,%d,%d,%d,%d,%d>'%(eye,servo,ear,M1arduino,Dir1,M2arduino,Dir2)

            print(eye,count1)
            try:
                ser.write(serialstring)
            except:
                pass
               

            sleep(0.1) #limit the frequency to 10Hz              
        except KeyboardInterrupt:
            print("Stopping...")
            pygame.quit()

Dualshock4Init()
motors()    
