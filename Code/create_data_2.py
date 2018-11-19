# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:54:52 2018

@author: Philipp
"""

import pyedflib
import numpy as np
import glob
import os
from scipy import signal
import matplotlib.pyplot as plt

no_samples=800

def segment(t_before,t_after,sample_frequency,annotations,BI,EMG):
    
    #error flags
    err_flag_start=0
    err_flag_end=0
    
    #check if window start index of the first segment is negative
    if((int(sample_frequency*annotations[0][0])-int(sample_frequency*t_before)) <0):
        err_flag_start=1
    
    #check if window end index of the last segment is positive
    if((int(sample_frequency*annotations[0][annotations[0].size-1])+int(sample_frequency*t_after)) > BI.size):
        err_flag_end=1    
    
    segment_length=int(sample_frequency*t_before)+int(sample_frequency*t_after)
    
    #define data array accordingly to the error flags
    segments=np.zeros((annotations[0].size-err_flag_start-err_flag_end, 2,segment_length))
    
    for i in range (0, annotations[0].size-err_flag_start-err_flag_end):
        
        swallow_index= int(sample_frequency*annotations[0][i+err_flag_start])        
        
        segment_start =swallow_index-int(sample_frequency*t_before)
        
        segment_end  = swallow_index+int(sample_frequency*t_after)        
        
        segments[i,0,:]=BI[segment_start:segment_end]
        segments[i,1,:]=EMG[segment_start:segment_end]
        
    return segments, err_flag_start, err_flag_end

data=np.zeros((1,2,no_samples))

os.chdir('F:/SchluckDaten/01_Rohdaten/')
for folder in glob.glob('*'): 
    
    if(os.path.isdir('F:/SchluckDaten/01_Rohdaten/'+folder+'/')):
               
        os.chdir('F:/SchluckDaten/01_Rohdaten/'+folder+'/')  
        
        #img_right = (img_right - np.mean( img_right )) / np.std( img_right )
        
        for file in glob.glob('*_edited_triggerMarker_edited.bdf'):
            
            print(file)

            f = pyedflib.EdfReader('F:/SchluckDaten/01_Rohdaten/'+folder+'/'+file)
            n = f.signals_in_file
            signal_labels = f.getSignalLabels()
            sigbufs = np.zeros((n, f.getNSamples()[0]))
            for i in np.arange(n):
                sigbufs[i, :] = f.readSignal(i)
            
            
            BI = sigbufs[0]
            BI=(BI-np.mean(BI))/np.std(BI)
            EMG = sigbufs[1] 
            EMG=(EMG-np.mean(EMG))/np.std(EMG)
            
            annotations = f.readAnnotations()  
            
            file_duaration = f.getFileDuration()
            samples_number =f.getNSamples()[0]
            sample_frequency = samples_number/file_duaration
                  
            temp, err_flag_start, err_flag_end=segment(0.35,0.05,sample_frequency,annotations,BI,EMG)
            
            data=np.concatenate((data,signal.resample(temp,no_samples,axis=2)),axis=0)
                
            
np.save('C:/Users/phili/Desktop/Schluckerkennung/Schluckerkennung/Code/data', data[1:])