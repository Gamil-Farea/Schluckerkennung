# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 13:56:35 2018

@author: galaz
"""
import pyedflib
import numpy as np
import matplotlib as plt
#f = pyedflib.EdfReader("C:/Users/phili/Desktop/Schluckerkennung/10/10-6-Schlucktest_Mengen_edited_triggerMarker_edited.bdf")
f = pyedflib.EdfReader("/Users/enwelt/Documents/Biomedizinische Technik M.Sc./Semester 5/Projektpraktikum Automatisierungstechnik/Daten/10/10-6-Schlucktest_Mengen_edited_triggerMarker_edited.bdf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)
    
BI = sigbufs[0] 
EMG = sigbufs[1] 
annotations = f.readAnnotations()  

sample_frequency = int(f.getSampleFrequency(1))

def segment(t_after,t_before,sample_frequency,annotations,BI,EMG):
    
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
    segments=np.zeros((2, annotations[0].size-err_flag_start-err_flag_end, segment_length))
    
    for i in range (0, annotations[0].size-err_flag_start-err_flag_end):
        
        swallow_index= int(sample_frequency*annotations[0][i+err_flag_start])        
        
        segment_start =swallow_index-int(sample_frequency*t_before)
        
        segment_end  = swallow_index+int(sample_frequency*t_after)        
        
        segments[0,i,:]=BI[segment_start:segment_end]
        segments[1,i,:]=EMG[segment_start:segment_end]
        
    return segments, err_flag_start, err_flag_end
      
result, err_flag_start, err_flag_end=segment(0.05,0.5,4000,annotations,BI,EMG)   

fig = plt.pyplot.figure()
ax = fig.add_subplot(111)
numberofsegment='123456789012345678901234567890'

plots=annotations[0].size-err_flag_end-err_flag_start
for i in range(plots):
    ax = fig.add_subplot(2,plots,i+1)
    ax.plot(result[0,i])
    ax2 = fig.add_subplot(2,plots,(plots+i+1))
    ax2.plot(result[1,i])
    ax2.set_title('The: %s st'%numberofsegment[i])
