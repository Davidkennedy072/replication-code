# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:48:59 2018
@author: David

Extracts height, width, and aspect ratio from contour data
Compare attributes and accuracy
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from byimageplotcontour import loadsio, contourdata
from rankimagebydifficulty import getorder

if matdata is None: # Test if variable is saved in memory 
    matdata = loadsio() 

def contouranalysis(contournumber, trialtype = 'animal'):
    xcontcoord, ycontcoord = contourdata(matdata, trialtype, contournumber)
    width = np.amax(xcontcoord) - np.amin(xcontcoord)
    height = np.amax(ycontcoord) - np.amin(ycontcoord)
    return width, height

def ordercontouranalysis(trialtype = 'animal', 
                         orderfile = 'byanimalmetameraverage.xlsx'):
    ''' Uses contouranalysis() and getorder generator to create DataFrame
    for contours'''
    data = pd.DataFrame(columns = ['accuracy', 'width', 'height', 'aspect'])
    for contournum, contacc in getorder():
        width, height = contouranalysis(contournum, trialtype)
        data.loc[contournum] = [contacc, width, height, None]
    return data

if __name__ == '__main__':
    animalframe = ordercontouranalysis(trialtype = 'animal')
    metamerframe = ordercontouranalysis(trialtype = 'metamer')
    plt.hist(animalframe['width'])