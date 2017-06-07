# Python 2.7 code to analyze sound and output volume levels

import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy   # from http://numpy.scipy.org/
import audioop

def volumelevels(): 
    chunk      = 2**11 # Change if too fast/slow, never less than 2**11
    scale      = 50    # Change if too dim/bright
    exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100 
 
    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device   = 0  
    
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
            level = int(level * 255)
 
            print (level)
       
    except KeyboardInterrupt:
        pass
    finally:
        print ("\nStopping")
        stream.close()
        p.terminate()
       

volumelevels()
