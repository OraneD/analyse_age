#from get_MFCCS_change import get_MFCCS_change



# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 08:45:25 2022

@author: Leonardo
"""
import numpy as np
from librosa.feature import mfcc
from librosa.core import load as audioLoad
from scipy import signal
from scipy.signal import find_peaks
import matplotlib.pyplot as plt



def get_MFCCS_change(filePath=None, channelN=0, sigSr=10000, tStep=0.005, winLen=0.025, n_mfcc=13, n_fft=512, removeFirst=1, filtCutoff=12, filtOrd=6):
    """ computes the amount of change in the MFCCs over time
    
    INPUT:
        
    filePath(default="./signals/audio/loc01_pert1_1_2_3_6_01.wav"
    channelN (default(default=0): selet the channel number for multichannel audio file
    sigSr (default=10000): frequency at which resampling the audio for the analysis
    tStep (default=0.005): analysis time step in ms
    winLen (default=0.025): analysis window length in ms
    n_mfcc (default=13): number of MFCCs to compute (the first one may then be removed via reoveFirst)
    n_fft (default=512): number of points for the FFT
    removeFirst (default=1): if one the first cepstral corefficient is dicarded
    filtCutoff (default=12): bandpass fitler freq.in Hz
    filtOrd (default=6): bandpass filter order
    
    OUTPUT:
    
    totChange: Amount of change over time
    T: time stamps for each value   
    """
    
    myAudio, _ = audioLoad(filePath,sr=sigSr, mono=False)
    
    if len(np.shape(myAudio))>1:
        y=myAudio[channelN,:]
    else:
        y=myAudio
    
    win_length=np.rint(winLen*sigSr).astype(int)
    hop_length=np.rint(tStep*sigSr).astype(int)
    
    
    myMfccs=mfcc( y=y, sr=sigSr, n_mfcc=n_mfcc, win_length=win_length, hop_length=hop_length,n_fft=n_fft)
    
    T=np.round(np.multiply(np.arange(1,np.shape(myMfccs)[1]+1),tStep)+winLen/2,4)
    
    if removeFirst:
       myMfccs=myMfccs[1:,:]
       
    cutOffNorm = filtCutoff / ((1/tStep) / 2)
    
    b1,a1 =signal.butter(filtOrd,cutOffNorm, 'lowpass')
    
    filtMffcs = signal.filtfilt(b1,a1,myMfccs)
    
    myAbsDiff=np.sqrt(np.gradient(filtMffcs,axis=1)**2)
    
    totChange=np.sum(myAbsDiff,0)
    
    totChange=signal.filtfilt(b1,a1,totChange)
    
    return totChange, T
    #plt.plot(totChange)










print(0)


spectralChange,timeStamps = get_MFCCS_change("../corpus_mfa_1channel/ESLO2_ENT_1001/ESLO2_ENT_1001_T1_2.wav")
print(spectralChange)
print(timeStamps)
peaks, _ = find_peaks(spectralChange)

median_peak_height = np.median(spectralChange[peaks])

filtered_peaks_indices = [peak for peak in peaks if spectralChange[peak] > median_peak_height and spectralChange[peak] > 0]
plt.figure(figsize=(12,7))
plt.plot(timeStamps, spectralChange, label='Cepstral Variation', color="blue")
plt.plot(timeStamps[filtered_peaks_indices], spectralChange[filtered_peaks_indices], "x", label='Peaks > median', color="red", markersize=10)
plt.axhline(y=median_peak_height, color="grey", linestyle="--", label='median')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('Cepstral Variation')
plt.title("Selection of cepstral peaks > median", fontsize=20, y=1.02)
plt.show()

mean_median_peaks = np.mean(spectralChange[filtered_peaks_indices])
print(mean_median_peaks)


#np.savetxt("output_19981209_0700_0800_franceinter_dga.txt",spectralChange)


