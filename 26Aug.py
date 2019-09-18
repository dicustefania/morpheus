# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:33:23 2019

@author: Stefania
"""
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
import os
from cmath import exp
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
    #print("cea mai apropiata putere a lui 2 de %s  este %s" %(N ,zeros))
    data_padded=np.append(data,[0 for j in range(zeros-N)])
    #print("lungime secventa after zero padding: %s" %len(data_padded))
    return data_padded


def quadratic_interpolation(y1,y2,y3):
    p = 1/2*(y1-y3)/(y1-2*y2+y3)
    yp = y2 - 1/4*(y1-y3)*p
    return(p,yp)
    
def linear_interpolation(y1, y2, n):
    y = (1-n)*y1 + n*y2
    return y

def spectral_mixing(y1,y2,n):
    mix = []
    mix_np = np.asarray(mix,dtype=complex)
    y1_np = np.asarray(y1,dtype=complex)
    y2_np = np.asarray(y2,dtype=complex)
    for elem1,elem2 in zip(y1_np,y2_np):
        mix_np = np.append(mix_np,(1-n)*elem1+n*elem2)
    return mix_np



os.chdir(r"C:\Users\Stefania\stefi_work\morpheus\inregistrari")
fs,data_ga=wavfile.read('GA001.wav')
data_ga1=zero_padding(data_ga)
N_ga=len(data_ga1)


#fft 
fft_ga=scipy.fft(data_ga1)
ampl_ga=abs(fft_ga)
phase_ga=np.unwrap(np.angle(fft_ga))
freqs_ga = scipy.fftpack.fftfreq(N_ga,1.0/fs)
#plt.plot(freqs_ga,ampl_ga)
#plt.xlim(0,fs/2)
ampl_ga1=ampl_ga[0:int(N_ga/2)]

#find peaks and plot
#peaks_ga,prop_ga=signal.find_peaks(ampl_ga[70*N_ga//fs:8000*N_ga//fs], distance=80*N_ga//fs)
peaks_ga,prop_ga=signal.find_peaks(ampl_ga1, distance=30*N_ga//fs)

#indice k cu amplitudine max si FF corespunzatoare
k=np.argmax(ampl_ga1)
ff_ga=k*fs/N_ga

#armonicele si fazele corespunzatoare 
harm_ga=[]
harm_ampl_ga=[]
harm_freq_ga=[]
i=2
while i*k<N_ga//2:
   
    harm_ga.append(i*k)
    harm_freq_ga.append(i*k*fs/N_ga)
    harm_ampl_ga.append(ampl_ga1[i*k])
    i=i+1

phase_ff_ga=phase_ga[k]
phase_harm_ga=[]
for elem in harm_ga:
    phase_harm_ga.append(phase_ga[elem])
    
#estimarea ff si armonicelor 
ff_e,y_ff_e=quadratic_interpolation(ampl_ga1[k-N_ga//fs],ampl_ga1[k],ampl_ga1[k+N_ga//fs])
FF_ga=(k+ff_e)*fs/N_ga

print('frecv fundamentala GA: ' %FF_ga)
harm_ga_e=[]
harm_ampl_ga_e=[]
harm_freq_ga_e=[]
for elem in harm_ga:
    x,y=quadratic_interpolation(ampl_ga1[elem-N_ga//fs],ampl_ga1[elem],ampl_ga1[elem+N_ga//fs])
    harm_ga_e.append(elem+x)
    harm_freq_ga_e.append((elem+x)*fs/N_ga)
    harm_ampl_ga_e.append(y)
    
#estimarea fazelor

phase_ff_ga_e = linear_interpolation(phase_ga[int(FF_ga*N_ga//fs)], phase_ga[int(FF_ga*N_ga//fs)+int(N_ga//fs)],FF_ga-int(FF_ga))
phase_harm_ga_e=[]
for elem in harm_freq_ga_e:
    phase_harm_ga_e.append(linear_interpolation(phase_ga[int(elem*N_ga//fs)], phase_ga[int(elem*N_ga//fs)+1],elem-int(elem)))    
    
#CC part
#read CC file
fs_cc,data_cc=wavfile.read('GA001.wav')
#data_cc1=zero_padding(data_cc)
N=len(data_cc)
N_frame=0.025*fs_cc
ham=np.hamming(N_frame)
frames=np.split(data_cc,80)
frames=frames*ham

new_audio=np.empty(1)
#steps b-g
for frame in frames:
    
    frame_pad=zero_padding(frame)
    N_cc=len(frame_pad)

#fft 
    fft_cc=scipy.fft(frame_pad)
    ampl_cc=abs(fft_cc)
    phase_cc=np.unwrap(np.angle(fft_cc))
    freqs_cc = scipy.fftpack.fftfreq(N_cc,1.0/fs)
    #plt.figure()
    #plt.plot(freqs_cc,cc_ampl)
    #plt.xlim(0,fs/2)
    ampl_cc1=ampl_cc[0:int(N_cc/2)]
    
    #find peaks and plot
    peaks_cc,prop=signal.find_peaks(ampl_cc1,distance=int(80*N_cc/fs))
    bins=[x+80*N_cc//fs_cc for x in peaks_cc]

    
    #indice k cu amplitudine max si FF corespunzatoare
    k_cc=np.argmax(ampl_cc1)
    ff_cc=k_cc*fs/N_cc
    #print("frecv fundamentala este %s Hz" %ff)
    
    #armonicele si fazele corespunzatoare 
    harm_cc=[]
    harm_ampl_cc=[]
    harm_freq_cc=[]
    j=2
    while j*k_cc<N_cc//2:
       
        harm_cc.append(j*k_cc)
        harm_freq_cc.append(j*k_cc*fs/N_cc)
        harm_ampl_cc.append(ampl_cc1[j*k_cc])
        j=j+1
    
    phase_ff_cc=phase_cc[k_cc]
    phase_harm_cc=[]
    for elem in harm_cc:
        phase_harm_cc.append(phase_cc[elem])
       
    #estimarea ff si armonicelor 
    ff_e_cc,y_ff_e_cc=quadratic_interpolation(ampl_cc1[k_cc-1],ampl_cc1[k_cc],ampl_cc1[k_cc+1])
    FF_cc=(k_cc+ff_e_cc*N_cc/fs)*fs/N_cc
    
    #print(FF_cc)
    harm_cc_e=[]
    harm_ampl_cc_e=[]
    harm_freq_cc_e=[]
    for elem in harm_cc:
        x_cc,y_cc=quadratic_interpolation(ampl_cc1[elem-1],ampl_cc1[elem],ampl_cc1[elem+1])
        harm_cc_e.append(elem+x_cc*N_cc//fs)
        harm_freq_cc_e.append((elem+x_cc*N_cc//fs)*fs/N_cc)
        harm_ampl_cc_e.append(y_cc)
        
    #estimarea fazelor
    
    phase_ff_e_cc = linear_interpolation(phase_cc[int(FF_cc*N_cc//fs)], phase_cc[int(FF_cc*N_cc//fs)+int(N_cc//fs)],FF_cc-int(FF_cc))
    phase_harm_e_cc=[]
    for elem in harm_freq_cc_e:
        phase_harm_e_cc.append(linear_interpolation(phase_cc[int(elem*N_cc//fs)], phase_cc[int(elem*N_cc//fs)+1],elem-int(elem)))    
        
    resample_factor=FF_cc/FF_ga
    
    resample_data=scipy.signal.resample_poly(data_ga,int(FF_cc),int(FF_ga))
    
    #mapping indices
    mapp_indexes=[]
    for i in range(len(harm_ga)):
        mapp_indexes.append(int(i/resample_factor+0.5))
    
    #frequency shifts
    di=[]
    for i in range(len(harm_ga)):
        di.append(int(FF_cc*(mapp_indexes[i]-1)*N_cc/fs+0.5))
    
    #gains
    gains=[]
    for elem1,elem2 in zip(harm_ampl_cc_e,harm_ampl_ga_e):
          gains.append(elem1/elem2)  
    
    #phase corrections
    phase_cor=[]
    for elem1,elem2 in zip(phase_harm_e_cc,phase_harm_ga_e):
          phase_cor.append(elem1/elem2)      
    
    
    
    N_res=len(resample_data)
    Y_res=abs(scipy.fft(resample_data))
    freq_res=scipy.fftpack.fftfreq(N_res,1.0/fs)

    Y_res1=Y_res[0:N_res//2]
    #peaks_res,prop=signal.find_peaks(Y_res1)
    new_bins = [int((freq * N_res)/fs) for freq in harm_freq_cc_e]
    
    Y=np.empty(N_cc,dtype=complex)
    
    for b, f, d, g, ph in zip(bins, new_bins, di, gains, phase_cor):
                Y[d] = Y_res[int(f)+d]*g*exp(1j*ph)
                print(b)
                print(int(f)+d)
    
    #plt.figure()
    #plt.plot(Y)
    Y_mix=np.empty(fft_cc.size,dtype=complex)
    Y_mix=spectral_mixing(Y,fft_cc,1)
    mix=scipy.fftpack.ifft(Y_mix)
    
    new_audio=np.concatenate((mix,new_audio))
    
scipy.io.wavfile.write('GM001.wav',fs,new_audio.astype('int16'))





#ploting
plt.plot(freqs_ga,ampl_ga)
plt.xlim(0,fs/2)
plt.title('spectru amplitudine GA wav')

plt.figure()
plt.plot(ampl_ga)
plt.xlim(0,fs)
plt.plot(peaks_ga,ampl_ga[peaks_ga],'x')
plt.title('spectru amplitudine GA wav plus varfuri')

plt.figure()
plt.plot(ampl_cc)
plt.xlim(0,N_cc/2)
plt.plot(peaks_cc,ampl_cc[peaks_cc],'x')
plt.title('spectru amplitudine frame CC plus varfuri')

plt.figure()
plt.plot(freq_res,Y_res)
plt.xlim(0,fs/2)
plt.title('spectru resampled')
plt.figure()
plt.plot(Y_res)
plt.xlim(0,N_res/2)
plt.title('spectru resampled in fct de N')

 
plt.figure()
plt.plot(abs(Y))
plt.title('spectru sintetizat')

plt.figure()
plt.plot(abs(Y_mix))
plt.title('spectrul mixat')