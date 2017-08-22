#! /usr/bin/python
import os  
import pygame
import pygame.mixer
from time import sleep
import sys
import pyaudio
import numpy
import audioop
import math
import serial

global ser
ser = serial.Serial('/dev/rfcomm0')
#setting up counter for press down events
global count
count = 0

global count1
count1 = 0

global count2
count2 = 0
global eye
eye = 0
global speed
speed = 0
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

Channel = pygame.mixer.Channel(0)

print ("Soundboard loaded")

# set up the window
screen = pygame.display.set_mode((630,630))
pygame.display.set_caption('DALEK')
bg = pygame.image.load("/home/chris/Desktop/Dalek-master/soundboard/background2.jpg")
screen.blit(bg,(0,0))
basicfont = pygame.font.SysFont(None, 48)


global DS4 #create global variable
global sound

def Connect():
    global ser
    global serialstring
    serialstring = '<0,0,0,0,0,0,0>'
    connected = False
    while not connected:
        try:
            ser = serial.Serial("/dev/rfcomm0", baudrate=9600,timeout=5)
            beacon = ser.read()
            if beacon =='k':
                connected = True
                ser.write(serialstring)
                print 'Arduino Connected'
                return True
                break
            elif beacon =='*':
                ser.write('p')
                return False
                print 'Arduino Detected'
            else:
                return False
                ser.close()
                                
        except serial.SerialException as e:
            print(e)
            return False
            ser.close()
            pass
            

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
                    print("No joystick attached")
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


def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print( str(i)+'. '+dev['name'])
        i += 1

def volumelevels(): 
    chunk      = 2**11 # Change if too fast/slow, never less than 2**11
    scale      = 50    # Change if too dim/bright
    exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100 
    
 
    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device   = 3  
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
 
    try:
        while True:
            data  = stream.read(chunk,exception_on_overflow = False)
            
            # Old RMS code, will only show the volume
            
            rms   = audioop.rms(data, 2)
 
            level = min(rms / (2.0 ** 16) * scale, 1.0) 
            level = level**exponent 
            level = int(level * 255)
 
            return(level)
            #changes brightness based on audio level
            
    except KeyboardInterrupt:
        pass
    finally:
      
        stream.close()
        p.terminate()

def steering(x,y):
    # convert to polar
    r = math.hypot(x,y)
    t = math.atan2(y,x)

    #rotate by 45 degrees
    t+= math.pi/4

    #back to cartesian
    left = r*math.cos(t)
    right = r*math.sin(t)

    #rescale new coordinates
    left= left*math.sqrt(2)
    right = right*math.sqrt(2)

    #clamp to -1/+1
    left = max(-1,min(left,1))
    right = max(-1,min(right,1))

    return(left,right)
        
def GUI(eye,servo,ear,M1arduino,Dir1,M2arduino,Dir2,parked,brakes,speed,sound,LW,RW,status):
    # set up the window
    screen = pygame.display.set_mode((800,480))
    pygame.display.set_caption('DALEK')
    bg = pygame.image.load("/home/chris/Desktop/Dalek-master/soundboard/background2.jpg")
    basicfont = pygame.font.SysFont(None, 30)
    earcolor = (ear,ear,0)
    eyecolor =pygame.Color(0,0,eye)
    radius = int((100-servo)/3.4)
    (DirL,AmpL) = LW
    (DirR,AmpR) = RW
    screen.blit(bg,(0,0))
    pygame.draw.circle(screen, (0,0,0), (168, 48), 35, 0)
    pygame.draw.circle(screen, eyecolor, (168, 48), radius, 0)
    pygame.draw.polygon(screen,earcolor,[(45,57),(69,31),(29,10),(13,26)],0)
    pygame.draw.polygon(screen,earcolor,[(289,57),(321,26),(305,10),(265,31)],0)
    #0 is reverse, 1 is forward
    if DirL ==1:
        pygame.draw.polygon(screen,(0,0,255),[(585,215),(603,215),(594,215-AmpL)],0)
    elif DirL ==0:
        pygame.draw.polygon(screen,(0,0,255),[(585,215),(603,215),(594,215+AmpL)],0)
    if DirR ==1:
        pygame.draw.polygon(screen,(0,0,255),[(751,215),(769,215),(760,215-AmpR)],0)
    elif DirR ==0:
        pygame.draw.polygon(screen,(0,0,255),[(751,215),(769,215),(760,215+AmpR)],0)
    if parked:
        pygame.draw.circle(screen, (255,0,0), (740, 343),7, 0)
    elif not parked:
        pygame.draw.circle(screen, (0,255,0), (740, 400),7, 0)
    if brakes:
        pygame.draw.circle(screen, (255,255,0), (740, 370),7, 0)
    if parked:
        pygame.draw.rect(screen,(255,0,0),[490,75,60,200],0)
    else:
        pygame.draw.rect(screen,(0,255,0),[490,(275-(speed*2)),60,(speed*2)],0)
    pygame.draw.rect(screen,(0,0,0),[490,75,60,200],2)
    text1 = basicfont.render(sound,1,(0,0,255))
    text2 = basicfont.render(status,1,(0,0,255))
    screen.blit(text1,(102,228))
    screen.blit(text2,(150,255))

    pygame.display.update()

def domemotors(RSLR,RSUD): # function takes in R stick DS4 data and outputs information for dome motors
    RSLR = int(RSLR*99)
    RSLRamp = abs(RSLR)
    RSUD = int(RSUD*99)
    RSUDamp = abs(RSUD)
    Dir1 = 0
    Dir2 = 0
    if RSLR>=0:
        Dir1 = 0
    else:
        Dir1 = 1       
    if RSUD>=0:
        Dir2 = 0 #alter these two parameters to change up/down direction of eyestalk
    else:
        Dir2 = 1
    M1arduino = int(RSLRamp*2.5)
    M2arduino = int(RSUDamp)
    return (M1arduino,Dir1,M2arduino,Dir2)

def fronteye(Dpad): #controls brightness of front eye using DS4 hat buttons
    global count1
    global eye
    
    if count1<99:
        eye = int(count1*2.5)
        count1 = count1+1
    elif count1>=99 and count1<200:
        eye = int(350-count1)
        count1 = count1+1
    elif count1>=200:
        if eye>255:
            eye = 255                    
        elif eye<0:
            eye = 0                    
        elif eye<=250 and (Dpad == (-1,1) or Dpad == (0,1) or Dpad == (1,1)):
            eye = eye +5                    
        elif eye>=5 and (Dpad == (-1,-1) or Dpad == (0,-1) or Dpad == (1,-1)):
            eye = eye-5
        else:
            eye=eye
    return (eye)

def iris(R3,R2): #controls iris servo movement from DS4 R2 and R3
    servo = 0
    amplitude = int((R2+1)*50)
    if R3:
        servo = 100
    else:
        servo = amplitude
    return(servo)

def soundboard(L1,Options,Triangle,Circle,Square,X): #takes in button presses and plays sound clips, returning string of sound clip
    global sound
    if Options and pygame.mixer.get_busy(): #pressing options button will stop playback
        pygame.mixer.stop()
    elif not pygame.mixer.get_busy(): #if sound is already playing, then dont acknowledge button presses
        sound = 'No Sound Playing'
        if L1:
            if Triangle:
                Channel.play(sndE)
                sound = 'R2D2'
            elif Circle:
                Channel.play(sndF)
                sound = 'Tardis'
            elif Square:
                Channel.play(sndG)
                sound = 'Dr. Who Theme'
            elif X:
                Channel.play(sndH)
                sound = 'INTRUDER'
        elif Triangle:
            Channel.play(sndA)
            sound = 'Obey'
        elif Circle:
            Channel.play(sndB)
            sound = 'You will be EXTERMINATED'
        elif Square:
            Channel.play(sndC)
            sound = 'EXTERMINATE ANNIHILATE DESTROY'
        elif X:
            Channel.play(sndD)
            sound = 'EMERGENCY'
    return(sound)

def wheelchairmotors(L3,LSLR,LSUD,Dpad):
    global count
    global speed
    global parked
    global driving
    global brakes
    DirL = 1
    DirR = 1
    AmpL = 0
    AmpR = 0
    #parking vs driving
    if L3 and count>=20:
        if parked and not driving:
            driving = True
            parked = False 
            count = 0
            speed = 0
        elif driving and not parked:
            driving = False
            parked = True
            count = 0
        else:
            driving = False                    
            parked = True
            count = 0
    elif L3 and count<=19:
        count = int(count+1)
    else:
        count = 0
                
    #wheelchair motors
           
    if parked:
        brakes = True
        
    elif driving and not L3:
        brakes = False
        steering
        (AmpL,AmpR) = steering(LSLR,LSUD)
        if AmpL>=0:
            DirL = 1
        else:
            DirL = 0       
        if AmpR>=0:
            DirR = 0 #alter these two parameters to change up/down direction of eyestalk
        else:
            DirR = 1
                    
    elif driving and L3:
        brakes = True
           
                        
    if speed<=95 and (Dpad == (1,0) or Dpad == (1,-1) or Dpad == (1,1)):
        speed = speed +5                    
    elif speed>=5 and (Dpad == (-1,0) or Dpad == (-1,1) or Dpad == (-1,-1)):
        speed = speed-5
    else:
        speed=speed
    
    AmpL = int(abs(AmpL)*speed)
    AmpR = int(abs(AmpR)*speed)
    if AmpL ==0 and AmpR ==0:
        brakes = True
   
    LW =(DirL,AmpL)#(direction,amplitude) of Left Wheel
    RW = (DirR,AmpR)#(direction,amplitude) of Right Wheel
        
    return(speed,parked,brakes,LW,RW)
        

def sendtoarduino(serialstring):
    global ser
    try:
        ser.write(serialstring)
        status = 'Yes'
    except:
        status = 'No'
        pass
    return(status)

    
def main():
    global DS4
    global serialstring
    global count
    global count1
    global count2
    global parked
    global driving
    global brakes
    global eye
    global speed
    print ('Press CTRL+C to quit')
    done = False
    
    
    '''
    chunk      = 2**10 # Change if too fast/slow, never less than 2**11
    scale      = 30   # Change if too dim/bright
    exponent   = 8     # Change if too little/too much difference between loud and quiet sounds
    samplerate = 48000
    device =0
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
                    '''
                    
    if not DS4.get_init():
        print("re-initializing controller")
        DS4.init()
    elif DS4.get_init():
        print("DS4 Initialized")
    else:
        print("WTF?")
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break # break out of the for loop
        if done:
            break
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
           

            #code for ear lights
            '''
            data  = stream.read(chunk,exception_on_overflow = False)
            rms   = audioop.rms(data, 2)
 
            level = min(rms / (2.0 ** 16) * scale, 1.0) 
            #level = level**exponent
            print(level)
            ''' 
            if R1:
                ear=int(255)
            else:
                ear = volumelevels()
            earcolor = (ear,ear,0)
 
            
            
          
            (speed,parked,brakes,LW,RW) = wheelchairmotors(L3,LSLR,LSUD,Dpad)
                            
            (M1arduino,Dir1,M2arduino,Dir2) = domemotors(RSLR,RSUD)
            servo = iris(R3,R2)
            sound = soundboard(L1,Options,Triangle,Circle,Square,X)
            eye1 = fronteye(Dpad)
            serialstring = '<%d,%d,%d,%d,%d,%d,%d>'%(eye1,servo,ear,M1arduino,Dir1,M2arduino,Dir2)
            status = sendtoarduino(serialstring)
            GUI(eye1,servo,ear,M1arduino,Dir1,M2arduino,Dir2,parked,brakes,speed,sound,LW,RW,status)
                                    

            sleep(0.1) #limit the frequency to 10Hz              
        except KeyboardInterrupt:
            print("Stopping...")
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            
list_devices()
Dualshock4Init()
#Connect()
main()    
