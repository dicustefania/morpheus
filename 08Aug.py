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
#from numpy.fft import fft,fftfreq
from scipy.fftpack import fft, ifft,fftfreq
from scipy import signal


def FFT(data,fs):
    N=len(data)
    t = scipy.arange(0, N/fs, 1.0/fs) 
    Y = abs(scipy.fft(data))
    phase=np.unwrap(np.angle(scipy.fft(data)))
    freqs = scipy.fftpack.fftfreq(N,1.0/fs)
    plt.subplot(411)
    p1 = plt.plot(t, data, "g") # plotting the signal
    plt.xlabel('Time[s]')
    plt.ylabel('Amplitude')
    plt.subplot(412)
    
    p2 = plt.plot(freqs, Y, "r")
    plt.xlim(-fs/2,fs/2)    # plotting the complete fft spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.subplot(413)
    
    #Y1=np.fft.fftshift(Y)
    Y1=Y[range(int(N/2.0))]
    freqs1=freqs[range(int(N/2.0))]
    p3 = plt.plot(freqs1,Y1, "b") # plotting the positive fft spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')
    plt.xlim(0,fs/2)
    plt.subplot(414)
    p4=plt.plot(phase)
    plt.show()
    return Y,freqs,phase
    


def zero_padding(data):
    N=len(data)
    i=0
    while(2**i<N):
        i=i+1
    zeros=2**i
    print("cea mai apropiata putere a lui 2 de  este" ,N,zeros)
    data_padded=np.append(data,[0 for j in range(zeros-N)])
    print(len(data_padded))
    return data_padded

def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
    f is a vector and x is an index for that vector.
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)


            
os.chdir(r"C:\Users\Stefania\stefi_work\morpheus")
fs, data = wavfile.read('audio1.wav')
data0 = data[:, 0]
print(len(data.shape))     #cate canale are intregul fisier

seg_time=5                 #cate sec sa aiba segment
N=seg_time*fs              #cate esantioanele are segmentul    
morphe_sample=data0[0:N-1]
print(len(morphe_sample))

Ts=1.0/fs                  #sample period

morphe_sample_padded=zero_padding(morphe_sample)
Y,freqs,phase=FFT(morphe_sample_padded,fs)
Y=Y[range(int(N/2.0))]
freqs=freqs[range(int(N/2.0))]
peaks,prop=signal.find_peaks(Y,height=1e08)
#fft_peaks=int(peaks*fs/N)

#for elem in peaks:
#    fft_peaks.append(fs*elem/N)
plt.figure()
plt.plot(Y)
plt.xlim(0,N/2)
plt.plot(peaks,Y[peaks],'x')
plt.show()
j=np.argmax(Y)
print(j)
true_j=parabolic(np.log(Y),j)[0]
print(true_j)
k=2
harmonics=[]
harmonics_ampl=[]
while(k*j<N/2):
    harmonics.append(k*j)
    harmonics_ampl.append(Y[k*j])
    k=k+1
print(len(harmonics),len(harmonics_ampl))
phases=[]
true_harmonics_ampl=[]
for elem in harmonics:
    phases.append(phase[elem])
ff_phase=phase[j]

#magnitudes_peaks=[]
#for i in peaks:
#    magnitudes_peaks.append(Y[i])
#magnitude_max=max(magnitudes_peaks)
#FF,prop=signal.find_peaks(Y,height=magnitude_max-1)
#print(FF)
#
#print('frecv fundamentala este',FF,'si are amplitudinea',Y[FF])



#morphe_sample_padded=np.append(morphe_sample,[0 for i in range(len_zeros+1-N)])   #zero padding la final
    
#len_zeros=int(pow(2,math.ceil(math.log(N,2)))) 

#print(len_zeros)  #algoritm2-putere a lui 2
#M=len_zeros
#Mh=float((M-1)/2.0)
#for m in range(-Mh,Mh,1):                      #zero padding
#    if m>-N/2 and m<N/2:
#        morphe_sample_padded[m]=morphe_sample[m]
#    else:
#        morphe_sample_padded[m]=0

#print(len(morphe_sample_padded))
