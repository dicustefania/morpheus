# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:33:23 2019

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

def zero_padding(data):
    N=len(data)
    i=0
    while(2**i<N):
        i=i+1
    zeros=2**i
    print("cea mai apropiata putere a lui 2 de %s  este %s" %(N ,zeros))
    data_padded=np.append(data,[0 for j in range(zeros-N)])
    print("lungime secventa after zero padding: %s" %len(data_padded))
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
def quadratic_interpolation(f,m):
    p = 1/2*(f[m-1]-f[m+1])/(f[m-1]-2*f[m]+f[m+1])
    yp = f[m] - 1/4*(f[m-1]-f[m+1])*p
    return(p,yp)

os.chdir(r"C:\Users\Stefania\stefi_work\morpheus\inregistrari")
fs,data_GA=wavfile.read('GA001.wav')
data_GA1=zero_padding(data_GA)
N=len(data_GA1)

GA_fft=scipy.fft(data_GA1)
GA_ampl=abs(GA_fft)
GA_phase=np.angle(GA_fft)
freqs = scipy.fftpack.fftfreq(N,1.0/fs)

plt.plot(freqs,GA_ampl)
plt.xlim(0,fs/2)
GA_ampl1=GA_ampl[0:int(N/2)]
peaks,prop=signal.find_peaks(GA_ampl1,height=0.4e7)
plt.figure()
plt.plot(GA_ampl)
plt.xlim(0,N/2)
plt.plot(peaks,GA_ampl1[peaks],'x')

k=np.argmax(GA_ampl1)
ff=k*fs/N

#p_ga,yp_ga = quadratic_interpolation(GA_ampl1[peaks], k)

#ff_ga = abs((np.argmax(GA_ampl1[peaks]+p_ga)*fs/GA_ampl1[peaks].size))
#FF_x,FF_y=parabolic(np.log(GA_ampl),np.argmax(GA_ampl))
#ff=FF_x*fs/N
print("frecv fundamentala este %s Hz" %ff)
harm_ga=[]
harm_ampl_ga=[]
harm_ga_freq=[]
i=2
while i*k<N//2:
   
    harm_ga.append(i*k)
    harm_ga_freq.append(i*k*fs/N)
    harm_ampl_ga.append(GA_ampl1[i*k])
    i=i+1

phase_ff=GA_phase[k]
phase_harmonics=[]
for elem in harm_ga:
    phase_harmonics.append(GA_phase[elem])