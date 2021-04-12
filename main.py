#PLEASE USE HEADPHONES#
import pyaudio #To install go here: https://pypi.org/project/PyAudio/#
import sys, time
import numpy as np
import wave

n = -10 #Change the pitch by making it lower or higher, 0 is your regular voice. Please don't go any lower than -20 and higher than 20, as it can hurt your ears!#
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 41000
RECORD_SECONDS = 100 #The length of the recording#
swidth = 2

p = pyaudio.PyAudio()
stream = p.open(format = FORMAT, channels = CHANNELS,rate = RATE,input = True, output = True,frames_per_buffer = chunk)


print("Currently recording")

start = time.time()
while time.time() - start < RECORD_SECONDS:

    data = stream.read(chunk)
    data = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))


    data = np.fft.rfft(data)
    

    data2 = [0]*len(data)
    if n >= 0:
        data2[n:len(data)] = data[0:(len(data)-n)]
        data2[0:n] = data[(len(data)-n):len(data)]
    else:
        data2[0:(len(data)+n)] = data[-n:len(data)]
        data2[(len(data)+n):len(data)] = data[0:-n]
    
    data = np.array(data2)

    data = np.fft.irfft(data)
    
    dataout = np.array(data, dtype='int16') 
    chunkout = wave.struct.pack("%dh"%(len(dataout)), *list(dataout)) #convert back to 16-bit data
    stream.write(chunkout)

    


print("Recording finished")

stream.stop_stream()
stream.close()
p.terminate()
