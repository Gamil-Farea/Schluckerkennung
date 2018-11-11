# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 13:56:35 2018

@author: galaz
"""

import pyedflib
import numpy as np
import matplotlib as plt
f = pyedflib.EdfReader("C:/Users/phili/Desktop/Schluckerkennung/1/1-12-Schlucktest_Leitfaehigkeit_edited_triggerMarker_edited.bdf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)
    
BI = sigbufs[0] 
EMG = sigbufs[1] 
annotations = f.readAnnotations()  
sample_frequency= 4000  

def segment(t_after,t_befor,sample_frequency,annotations,BI,EMG):
    BI_segment_list = []
    EMG_segment_list = []
    for i in range (annotations[0].size):
        BI_segment = []
        EMG_segment = []
        swallow_index= int(sample_frequency*annotations[0][i])
        segment_start =swallow_index-int(sample_frequency*t_befor)
        segment_end  = swallow_index+int(sample_frequency*t_after)
        segment_length = segment_end-segment_start
        for j in range (segment_length):
            BI_segment.append(BI[segment_start+j])
            EMG_segment.append(EMG[segment_start+j])
        BI_segment_list.append(BI_segment)    
        EMG_segment_list.append(EMG_segment)  
    return [BI_segment_list, EMG_segment_list] 
      
result=segment(2,0.5,4000,annotations,BI,EMG)   

fig = plt.pyplot.figure()
ax = fig.add_subplot(111)
numberofsegment='123456'

for i in range(annotations[0].size):
    ax = fig.add_subplot(2,annotations[0].size,i+1)
    ax.plot(result[0][i])
    ax = fig.add_subplot(2,annotations[0].size,(annotations[0].size+i+1))
    ax.plot(result[1][i])
    ax.set_title('The: %s st'%numberofsegment[i])


