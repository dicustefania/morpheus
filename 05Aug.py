# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 19:14:23 2019

@author: Stefania
"""
import matplotlib.pyplot as plt
import scipy 
from scipy.io import wavfile
import os
import numpy as np
from numpy.fft import fft,fftfreq
#from scipy.fftpack import fft, ifft,fftfreq

os.chdir(r"C:\Users\Stefania\stefi_work")
fs, data = wavfile.read('monster growl 2.wav')
date=list(data)
Ts=1.0/fs #sample period
print(len(data.shape)) #cate canale

N=data.shape[0] #esantioanele primului canal
print(N)

secs=N/float(fs) #durata in sec a wav file
print(secs)

t = scipy.arange(0, secs, Ts) 
FFT = abs(scipy.fft(data))
FFT_side = FFT[range(int(N/2))]
freqs = scipy.fftpack.fftfreq(data.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(int(N/2))] # one side frequency range
fft_freqs_side = np.array(freqs_side)

plt.subplot(311)
p1 = plt.plot(t, data, "g") # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.subplot(312)
p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')
plt.subplot(313)
p3 = plt.plot(freqs_side, abs(FFT_side), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
plt.show()

x=1
len_morph=x*fs
morphe_sample=data[0:len_morph-1]
print(len(morphe_sample))
for i in range(len_morph-1):
    morphe_sample=np.append(morphe_sample,[data[i]])
    #morphe_sample.append(date[i])

len_zeros=len_morph
i=0
while(2**i<len_zeros):
    i=i+1
len_zeros=2**i
print(len_zeros)
        
#for i in range(len_morph-1,len_zeros):
new_morphe_sample=np.append(morphe_sample,[0 for i in range(len_morph-1,len_zeros)])
    
print(len(new_morphe_sample))
##print(morphe_sample)
#



