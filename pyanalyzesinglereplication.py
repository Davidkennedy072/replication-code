# -*- coding: utf-8 -*-
"""
Created on Wed May  9 11:37:05 2018

@author: zae
"""


import scipy.io as sio
import numpy as np
import os 
import matplotlib.pyplot as plt 

# Collect data into python
filelist = []
for root, dirs, files in os.walk('C:/Users/zae/Documents/summer2018/DY_data'):
    for file in files:
        if file.endswith('.mat'):
            filelist.append(file)
for file in filelist:
    pass
matdata = sio.loadmat('replicationDY16052012-1542.mat')
versioninfo = matdata['__header__']
dataresponse = matdata['response'][0][0]
# Data
responses = dataresponse['Data'][0][0]['Response']
lineinfo = dataresponse['Data'][0][0]['lineInfo']
maskingLine = dataresponse['Data'][0][0]['maskingLine']
distrators = dataresponse['Data'][0][0]['numDistractors']

#Remake data structure as 2D numpy. 7 by 50
blocksdata = dataresponse['currentBlock'][0][0] - 1 # 7
trials = dataresponse['numTrialsPerBlock'][0][0] # 50
response2D = np.zeros([blocksdata, trials], dtype = float)
for block in np.arange(blocksdata):
    response2D[block,:] = responses[0][block]
print('# of data points: {}'.format(response2D.size))
#Delays used in the experiment
timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0]) 
# np.unique =  Unique sorted order of matrix 

accuracy = {} # Set accuracy as a python dict 
nDist = {}

for j in range(len(timeSeq)): # Add part to match block to timeSeq later
    blocks = np.where(dataresponse['fixationDisplayTimeSeq'][0] == timeSeq[j])[0]
    print(blocks) # Shift of 1 because of index 0 compared to matlab index 1
    
    for b in range(len(blocks)): # 1 in the case of DY
        gt = dataresponse['imageObjectFlagSeq'][0][blocks[b]][0]
        resp = response2D[blocks[b]]
        
        #Accuracy
        correct = np.equal(gt, resp)
        accuracy[j, b] = np.mean(correct)
        
        #Distractors 
        QUESTdist = distrators[0][blocks[b]]
        nDistFinal = QUESTdist[0][-1]
        nDist[j, b] = nDistFinal
