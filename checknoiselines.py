# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:48:07 2018
@author: David
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy.io as sio 
import random

#Get data
filelist = []
for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.mat'):
                    filelist.append(file)
filelist = [item for item in filelist if 'replication' in item]
file = random.choice(filelist)
matdata = sio.loadmat(file)
dataresponse = matdata['response'][0][0]
lengthframe = pd.DataFrame(columns = ['block', 'trial', 'imageflag', 'averagelength', 'std'])
for blocks in range(dataresponse['currentBlock'][0][0] - 1):
    for trials in range(dataresponse['numTrialsPerBlock'][0][0]):
        imageflag = dataresponse['imageObjectFlagSeq'][0][blocks][0][trials] # One for animal 0 for metamer
        avglength = []
        avgstd = []
        for frame in range(100):
            maskinglines = dataresponse['Data'][0][0]['maskingLine'][0][blocks-1][0][trials-1][0][frame] # subtract 1 because Matlab starts with index 1
            maskinglinex = maskinglines[0]
            linex = []
            linex.append(maskinglinex[::2])
            linex.append(maskinglinex[1::2])
            maskingliney = maskinglines[1]
            liney = []
            liney.append(maskingliney[::2])
            liney.append(maskingliney[1::2])
            lengthx = linex[0]- linex[1] 
            lengthy = liney[0] - liney[1]
            length = []
            
            for element in range(len(lengthx)):
                length.append((lengthx[element]**2+lengthy[element]**2)**(1/2))
        avglength.append(np.mean(length))
        avgstd.append(np.std(length))
        averagelength = np.mean(avglength)
        averagestd = np.mean(avgstd)
        lengthframe.loc['{}.{}'.format(blocks, trials)] = [blocks, trials, imageflag, averagelength, averagestd]
animalaverage = lengthframe.loc[lengthframe['imageflag'] == 1]['averagelength'].mean()
animalstd = lengthframe.loc[lengthframe['imageflag'] == 1]['averagelength'].std()
metameraverage = lengthframe.loc[lengthframe['imageflag'] == 0]['averagelength'].mean()
metamerstd = lengthframe.loc[lengthframe['imageflag'] == 0]['averagelength'].std()
fig, ax = plt.subplots()
ax.bar(0, metameraverage, yerr = metamerstd)
ax.bar(1, animalaverage, yerr = animalstd)
ax.set_xticks([0,1])
ax.set_xticklabels(['metamer', 'animal'])
plt.title('animal = {:.4f},std = {:.4f}. metamer = {:.4f}, std = {:.4f}'.format(animalaverage, animalstd, metameraverage, metamerstd))
plt.suptitle(file[-46:])

animalstd = lengthframe.loc[lengthframe['imageflag'] == 1]['std'].mean()
animalstdstd = lengthframe.loc[lengthframe['imageflag'] == 1]['std'].std()
metamerstd = lengthframe.loc[lengthframe['imageflag'] == 0]['std'].mean()
metamerstdstd = lengthframe.loc[lengthframe['imageflag'] == 0]['std'].std()
fig, ax = plt.subplots()
ax.bar(0, metamerstd, yerr = metamerstdstd)
ax.bar(1, animalstd, yerr = animalstdstd)
ax.set_xticks([0,1])
ax.set_xticklabels(['metamer std', 'animal std'])
plt.title('animal = {:.4f},std = {:.4f}. metamer = {:.4f}, std = {:.4f}'.format(animalstd, animalstdstd, metamerstd, metamerstdstd))
plt.suptitle(file[-46:] +'_std')