# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 15:54:52 2018

@author: Philipp
"""

import pyedflib
import numpy as np
import matplotlib as plt

path='F:/SchluckDaten/01_Rohdaten/'
path_end='_edited_triggerMarker_edited.bdf'

paths=['1/1-12-Schlucktest_Leitfaehigkeit', '1/1-13-Schlucktest_Mengen', '1/1-14-Schlucktest_Mengen', '1/1-15-Schlucktest_Mengen', 
       '1/1-16-Schlucktest_Mengen', '1/1-17-Schlucktest_Mengen', '1/1-18-Schlucktest_Mengen', '1/1-19-Schlucktest_Mengen', 
       '1/1-34-Schlucktest_Mengen', '1/1-36-Schlucktest_Mengen', '3/3-1-Schlucktest_Leitfaehigkeit', '3/3-2-Schlucktest_Mengen', 
       '3/3-3-Bewegung_edited', '3/3-4-Schlucktest_Mengen', '3/3-5-Schlucktest_Mengen', '3/3-6-Schlucktest_Mengen',
       '3/3-7-Schlucktest_Mengen', '4/4-21-Bewegung', '4/4-51-Schlucktest_Leitfaehigkeit', '4/4-52-Schlucktest_Mengen',
       '4/4-53-Schlucktest_Leitfaehigkeit', '4/4-54-Schlucktest_Mengen', '4/4-55-Bewegung_edited', '4/4-87-Schlucktest_Mengen', 
       '4/4-88-Schlucktest_Mengen', '4/4-89-Schlucktest_Mengen', '4/4-94-Schlucktest_Mengen', '4/4-95-Schlucktest_Mengen',
       '4/4-96-Schlucktest_Mengen', '4/4-97-Schlucktest_Mengen', '4/4-98-Schlucktest_Mengen', '4/4-99-Schlucktest_Mengen',
       '4/4-100-Schlucktest_Mengen', '4/4-101-Schlucktest_Mengen', '4/4-102-Schlucktest_Mengen', '4/4-103-Schlucktest_Mengen', 
       '4/4-104-Schlucktest_Mengen', '4/4-105-Schlucktest_Mengen', '4/4-106-Schlucktest_Mengen', '4/4-107-Schlucktest_Mengen',
       '4/4-108-Schlucktest_Mengen', '5/5-1-Bewegung_edited', '5/5-4-Schlucktest_Leitfaehigkeit', '5/5-5-Schlucktest_Mengen',
       '5/5-6-Bewegung_edited', '5/5-10-Schlucktest_Mengen', '5/5-11-Schlucktest_Mengen', '5/5-12-Schlucktest_Mengen',
       '5/5-13-Schlucktest_Mengen', '5/5-14-Schlucktest_Mengen', '5/5-15-Schlucktest_Mengen', '5/5-16-Schlucktest_Mengen',
       '5/5-17-Schlucktest_Mengen', '6/6-1-Bewegung_edited', '6/6-4-Schlucktest_Leitfaehigkeit', '6/6-5-Schlucktest_Mengen',
       '6/6-6-Schlucktest_Mengen', '6/6-21-Schlucktest_Mengen', '6/6-22-Schlucktest_Mengen', '6/6-23-Schlucktest_Mengen', 
       '6/6-25-Schlucktest_Mengen', '6/6-26-Schlucktest_Mengen', '6/6-27-Schlucktest_Mengen', '6/6-28-Schlucktest_Mengen', 
       '6/6-30-Schlucktest_Mengen', '6/6-31-Schlucktest_Mengen', '7/7-1-Bewegung_edited', '7/7-4-Schlucktest_Leitfaehigkeit', 
       '7/7-5-Schlucktest_Mengen', '7/7-6-Bewegung_edited', '7/7-7-Schlucktest_Leitfaehigkeit', '7/7-8-Schlucktest_Mengen', 
       '7/7-9-Bewegung_edited', '7/7-10-Schlucktest_Mengen', '7/7-11-Schlucktest_Mengen', '7/7-12-Schlucktest_Mengen', 
       '7/7-16-Schlucktest_Mengen', '7/7-17-Schlucktest_Mengen', '7/7-18-Schlucktest_Mengen', '7/7-19-Schlucktest_Mengen', 
       '7/7-20-Schlucktest_Mengen', '8/8-1-Schlucktest_Leitfaehigkeit', '8/8-2-Schlucktest_Mengen', '8/8-3-Bewegung_edited', 
       '8/8-4-Schlucktest_Leitfaehigkeit', '8/8-5-Schlucktest_Mengen', '8/8-6-Bewegung_edited', '8/8-7-Schlucktest_Mengen', 
       '8/8-8-Schlucktest_Mengen', '8/8-9-Schlucktest_Mengen', '8/8-10-Schlucktest_Mengen', '8/8-11-Schlucktest_Mengen', 
       '8/8-12-Schlucktest_Mengen', '8/8-16-Schlucktest_Mengen', '8/8-17-Schlucktest_Mengen', '9/9-1-Schlucktest_Leitfaehigkeit', 
       '9/9-2-Schlucktest_Mengen', '9/9-3-Bewegung', '9/9-4-Schlucktest_Mengen', '9/9-5-Schlucktest_Mengen', 
       '9/9-6-Schlucktest_Mengen', '9/9-7-Schlucktest_Mengen', '9/9-8-Schlucktest_Mengen', '9/9-9-Schlucktest_Mengen', 
       '9/9-11-Schlucktest_Mengen', '9/9-12-Schlucktest_Mengen', '9/9-13-Schlucktest_Mengen', '9/9-14-Schlucktest_Mengen', 
       '10/10-1-Schlucktest_Leitfaehigkeit', '10/10-2-Schlucktest_Mengen', '10/10-3-Bewegung_edited', '10/10-4-Schlucktest_Mengen',
       '10/10-5-Schlucktest_Mengen', '10/10-6-Schlucktest_Mengen', '10/10-7-Schlucktest_Mengen', '11/11-1-Schlucktest_Leitfaehigkeit',
       '11/11-2-Schlucktest_Mengen', '11/11-3-Bewegung_edited', '11/11-4-Schlucktest_Leitfaehigkeit', '11/11-5-Schlucktest_Mengen',
       '11/11-6-Bewegung', '11/11-7-Schlucktest_Mengen', '11/11-8-Schlucktest_Mengen', '11/11-9-Schlucktest_Mengen', 
       '11/11-10-Schlucktest_Mengen', '11/11-11-Schlucktest_Mengen', '11/11-12-Schlucktest_Mengen', '11/11-13-Schlucktest_Mengen', 
       '11/11-14-Schlucktest_Mengen', '13/13-1-Schlucktest_Leitfaehigkeit', '13/13-2-Schlucktest_Mengen', '13/13-3-Bewegung_edited',
       '13/13-4-Schlucktest_Leitfaehigkeit', '13/13-5-Schlucktest_Mengen', '13/13-6-Bewegung', '13/13-7-Schlucktest_Mengen',
       '13/13-8-Schlucktest_Mengen', '13/13-9-Schlucktest_Mengen', '13/13-10-Schlucktest_Mengen', '13/13-11-Schlucktest_Mengen',
       '13/13-12-Schlucktest_Mengen', '13/13-13-Schlucktest_Mengen', '13/13-14-Schlucktest_Mengen', '14/']

f = pyedflib.EdfReader("F:/SchluckDaten/01_Rohdaten/21/21-1-Schlucktest_Leitfaehigkeit_edited_triggerMarker.bdf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)
    
BI = sigbufs[0] 
EMG = sigbufs[1] 
annotations = f.readAnnotations()  

file_duaration = f.getFileDuration()
smaples_number =f.getNSamples()[0]
sample_frequency = smaples_number/file_duaration



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
    segments=np.zeros((2, annotations[0].size-err_flag_start-err_flag_end, segment_length))
    
    for i in range (0, annotations[0].size-err_flag_start-err_flag_end):
        
        swallow_index= int(sample_frequency*annotations[0][i+err_flag_start])        
        
        segment_start =swallow_index-int(sample_frequency*t_before)
        
        segment_end  = swallow_index+int(sample_frequency*t_after)        
        
        
        
        segments[0,i,:]=BI[segment_start:segment_end]
        segments[1,i,:]=EMG[segment_start:segment_end]
        
    return segments, err_flag_start, err_flag_end
      
result, err_flag_start, err_flag_end=segment(0.35,0.05,4000,annotations,BI,EMG)   

fig = plt.pyplot.figure()
ax = fig.add_subplot(111)
numberofsegment='123456789012345678901234567890'

plots=annotations[0].size-err_flag_end-err_flag_start