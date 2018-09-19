# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:15:06 2018
@author: David
Generates excel based on requirements posed by Kris's email: 
    Representative animal/metamers pair
"""
import os
import numpy as np
import scipy.io as sio 
import pandas as pd
import matplotlib.pyplot as plt

excelcolumns = ['subjectID', 'delay', '#distractors', 'animal#', 'AnimalorMetamer', 'correct']
data = pd.DataFrame(columns = excelcolumns)

subjectlist = ['BC','CD', 'DY', 'HP', 'KAE', 'MD']
for subjectinital in subjectlist:
    trialtype = 'replication'
    filelist = []
    
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.mat'):
                if trialtype+subjectinital in file:
                    filelist.append(file)
    
    for file in filelist:
        counter = 0
        matdata = sio.loadmat(file)
        dataresponse = matdata['response'][0][0]
        responses = dataresponse['Data'][0][0]['Response']
        responses = responses[0] # User choice 1 = animal 0 = metamer
        distrators = dataresponse['Data'][0][0]['numDistractors'][0]
        blocksdata = dataresponse['currentBlock'][0][0] - 1 # 7
        trials = dataresponse['numTrialsPerBlock'][0][0] # 50
        
        timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0])
        delayLabel = []
        for j in range(len(timeSeq)):
            delayLabel.append(1000*timeSeq[j]+10)
        # Animal/ metamer information
        imageused = dataresponse['ImageUsedSeq'][0]
        imageobjectflagseq = dataresponse['imageObjectFlagSeq'][0] # 1 = animal 0 = metamer
#           whichsampleseq = dataresponse['whichSampleSeq'][0]
            
        correct = []
        for b in range(blocksdata):
            resp = responses[b][0]
            sol = imageobjectflagseq[b][0]
            correct.append(np.equal(resp, sol))
    
        for block in range(blocksdata):
            for trial in range(trials):
                toappend = [subjectinital, delayLabel[block], distrators[block][0][trial],
                            imageused[block][0][trial], imageobjectflagseq[block][0][trial],
                            correct[block][trial]]
                data.loc[file+str(block)+str(trial)] = toappend
writer = pd.ExcelWriter('animalmetamer.xlsx', engine = 'xlsxwriter')
data.to_excel(writer, sheet_name = 'data')
writer.save()