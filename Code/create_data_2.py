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

def segment_non_swallows(intervalls,segment_length,BI,EMG): 
    segments=np.zeros((1, 2,segment_length))
    
    for k in range(intervalls[:,0].size):
        length=intervalls[k,1]-intervalls[k,0]
        no_non_swallows=int(length/segment_length)
        
        if(no_non_swallows>0):
            start=np.random.randint(intervalls[k,0],intervalls[k,1]-segment_length*no_non_swallows+1)
        
            temp=np.zeros((no_non_swallows, 2,segment_length))
        
            for j in range(no_non_swallows):
                temp[j,0,:]=BI[start+segment_length*j:start+segment_length*(j+1)]
                temp[j,1,:]=EMG[start+segment_length*j:start+segment_length*(j+1)]
            
            segments=np.concatenate((segments,temp),axis=0)
    
    return segments[1:]

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
    
    if(segment_length<no_samples):
        print('Warning!')
        print('The data is being upsampled. The length of a segment of a signal is smaller than the number of samples used for the training!')
    
    #define data array accordingly to the error flags
    swallows=np.zeros((annotations[0].size-err_flag_start-err_flag_end, 2,segment_length))
    
    non_swallow_intervalls=np.zeros((annotations[0].size-err_flag_start-err_flag_end+1, 2))
    
    if(err_flag_start==1):
        non_swallow_intervalls[0,0]=sample_frequency*annotations[0][0]+int(sample_frequency*1.5)
    else:
        non_swallow_intervalls[0,0]=10
        
    if(err_flag_end==1):
        non_swallow_intervalls[annotations[0].size-1,1]=sample_frequency*annotations[0][annotations[0].size-1]-int(sample_frequency*0.5)  
    else:
        non_swallow_intervalls[annotations[0].size-1,1]=BI.size-10
    
    for i in range (0, annotations[0].size-err_flag_start-err_flag_end):
        
        swallow_index= int(sample_frequency*annotations[0][i+err_flag_start])        
        
        segment_start =swallow_index-int(sample_frequency*t_before)  
        segment_end  = swallow_index+int(sample_frequency*t_after)   
        
        non_swallow_intervalls[i+1,0]=swallow_index+int(sample_frequency*1.5) 
        non_swallow_intervalls[i,1]=swallow_index-int(sample_frequency*0.5)
        
        swallows[i,0,:]=BI[segment_start:segment_end]
        swallows[i,1,:]=EMG[segment_start:segment_end]
        
        
    non_swallows=segment_non_swallows(non_swallow_intervalls,segment_length,BI,EMG) 
        
    return swallows, non_swallows, err_flag_start, err_flag_end

data_swallow=np.zeros((1,2,no_samples))
data_non_swallow=np.zeros((1,2,no_samples))

path=['F:/SchluckDaten/01_Rohdaten/', 'F:/SchluckDaten/17_RehaIngest/', 'F:/SchluckDaten/17_RehaIngest/Hasomed_18_10/']

for p in path:
    os.chdir(p)
    for folder in glob.glob('*'): 
        
        if(os.path.isdir(p+folder+'/')):
                   
            os.chdir(p+folder+'/')  
            
            for file in glob.glob('*_edited_triggerMarker_edited.bdf'):
                print(file)
    
                f = pyedflib.EdfReader(p+folder+'/'+file)
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
                      
                temp1, temp2, err_flag_start, err_flag_end=segment(0.35,0.05,sample_frequency,annotations,BI,EMG)
                
                data_swallow=np.concatenate((data_swallow,signal.resample(temp1,no_samples,axis=2)),axis=0)
                data_non_swallow=np.concatenate((data_non_swallow,signal.resample(temp2,no_samples,axis=2)),axis=0)
            
np.save('C:/Users/phili/Desktop/Schluckerkennung/Schluckerkennung/Code/data_swallow', data_swallow[1:])
np.save('C:/Users/phili/Desktop/Schluckerkennung/Schluckerkennung/Code/data_non_swallow', data_non_swallow[1:])