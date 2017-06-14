# Python 2.7 code to analyze sound and output volume levels

import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy   # from http://numpy.scipy.org/
import audioop
import RPi.GPIO as GPIO
#setting up GPIO in broadcom mode, using pin 21 as output
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)

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
    scale      = 30   # Change if too dim/bright
    exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100
    led = GPIO.PWM(21, 100) #LED output pin 21 PWM mode at 100Hz
    led.start(0)
 
    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device   = 1 
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
    print ("Starting, use Ctrl+C to stop")
    try:
        while True:
            data  = stream.read(chunk,exception_on_overflow = False)
            
            # Old RMS code, will only show the volume
            
            rms   = audioop.rms(data, 2)
 
            level = min(rms / (2.0 ** 16) * scale, 1.0) 
            level = level**exponent 
            level = int(level * 100)
 
            print (level)
        
            #changes brightness based on audio level
            led.ChangeDutyCycle(level) 
    except KeyboardInterrupt:
        pass
    finally:
        print ("\nStopping")
        stream.close()
        p.terminate()
        led.stop()
        GPIO.cleanup()       

volumelevels()
