## -*- coding: utf-8 -*-
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
import math
from scipy.fftpack import fft, ifft,fftfreq

os.chdir(r"C:\Users\Stefania\stefi_work\morpheus")
fs, data = wavfile.read('monster growl 2.wav')
print(len(data.shape))     #cate canale are intregul fisier

seg_time=2                 #cate sec sa aiba segment
N=seg_time*fs              #cate esantioanele are segmentul    
morphe_sample=data[0:N-1]
print(len(morphe_sample))


Ts=1.0/fs                  #sample period

len_zeros=N                          #algoritm1 -aflarea celei mai apropiate mai mare putere a lui 2
                                                #len_zeros=cea mai apropiata putere a lui 2 
i=0
while(2**i<len_zeros):
    i=i+1
len_zeros=2**i
print(len_zeros)
        
morphe_sample_padded=np.append(morphe_sample,[0 for i in range(len_zeros+1-N)])   #zero padding la final
    
len_zeros=int(pow(2,math.ceil(math.log(N,2)))) 

#print(len_zeros)  #algoritm2-putere a lui 2
#M=len_zeros
#Mh=float((M-1)/2.0)
#for m in range(-Mh,Mh,1):                      #zero padding
#    if m>-N/2 and m<N/2:
#        morphe_sample_padded[m]=morphe_sample[m]
#    else:
#        morphe_sample_padded[m]=0


print(len(morphe_sample_padded))

t = scipy.arange(0, len_zeros*Ts, Ts) 
FFT = abs(scipy.fft(morphe_sample_padded))
FFT_side = FFT[range(int(N/2))]
freqs = scipy.fftpack.fftfreq(len_zeros, Ts)
fft_freqs = np.array(freqs)
freqs_side = freqs[range(int(N/2))] # one side frequency range
fft_freqs_side = np.array(freqs_side)

plt.subplot(311)
p1 = plt.plot(t, morphe_sample_padded, "g") # plotting the signal
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
