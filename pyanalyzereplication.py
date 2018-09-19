# -*- coding: utf-8 -*-
"""
Created on Fri May  4 16:53:36 2018

@author: David 
"""

import scipy.io as sio
import numpy as np
import os 
import matplotlib.pyplot as plt 

# Collect data into python
filelist = []
path = 'C:/Users/zae/Documents/summer2018/ReplicationData'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.mat'):
            filelist.append(file)
c = 0
filelist = ['replicationDY16052012-1542.mat']
accuracy = {}
nDist = {} # Set accuracy and nDist as Python Dict 
for file in filelist:
    
    matdata = sio.loadmat(file)
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
        timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0])
        # np.unique =  Unique sorted order of matrix 
        
        for j in range(len(timeSeq)): # Add part to match block to timeSeq later
            blocks = np.where(dataresponse['fixationDisplayTimeSeq'][0] == timeSeq[j])[0]
            
            for b in range(len(blocks)): # 1 in the case of DY
                gt = dataresponse['imageObjectFlagSeq'][0][blocks[b]][0]
                resp = response2D[blocks[b]]
                
                #Accuracy
                correct = np.equal(gt, resp)
                accuracy[j, b+c] = np.mean(correct)
                
                #Distractors 
                QUESTdist = distrators[0][blocks[b]]
                nDistFinal = QUESTdist[0][-1]
                nDist[j, b+c] = nDistFinal
    c = c + len(blocks)
delayLabel = []
timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0])
for j in range(len(timeSeq)-1):
    delayLabel.append(1000*timeSeq[j+1])
# Figures
'''
# Accuracy figures:
acc = np.zeros([len(timeSeq), len(filelist)]) 
# Convert accuracy and nDist from Dict to numpy array
for key, value in accuracy.items():
    acc[key[0], key[1]] = value
mean_acc = np.mean(acc,1)
plt.figure(1)
axes = plt.gca()
axes.set_ylim([0.5, 1])
plt.plot(timeSeq[1:], mean_acc[1:], color = 'red')
plt.plot(timeSeq[1:], np.full((len(timeSeq[1:]), 1), mean_acc[0]), color = 'green',
         linestyle = '--')
plt.xlabel('Delay')

for lines in range(acc.shape[1]):
    y = plt.plot(timeSeq[1:], acc[:, lines][1:])
    plt.setp(y, linestyle = ':', marker = '+', color = 'black')
plt.xticks(timeSeq[1:],np.array(delayLabel))
'''
#Distrators figures:
Dist = np.zeros([len(timeSeq), len(filelist)])
for key, value in nDist.items():
    Dist[key[0], key[1]] = value
mean_Dist = np.mean(Dist, 1)

plt.figure()
axes = plt.gca()
plt.plot(timeSeq, mean_Dist, color = 'red')
#plt.plot(timeSeq[1:], np.full((len(timeSeq[1:]), 1), mean_Dist[0]), color = 'green',
#         linestyle = '--')
plt.xlabel('Delay')
#for lines in range(Dist.shape[1]):
#    y = plt.plot(timeSeq[1:], Dist[:, lines][1:])
#    plt.setp(y, linestyle = ':', marker = '+', color = 'black')
