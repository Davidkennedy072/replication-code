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
import scipy as sp

from byimageplotcontour import loadsio, contourdata
from rankimagebydifficulty import getorder
from datastats import linearregression

path = 'C:/Users/zae/Documents/summer2018/ReplicationData/contourSegInfoAllPost_20.mat'
#matdata = loadsio(file = path) 
def savetotxt(pts, name):
    '''Takes pts and saves to txt for Matlab'''
    np.savetxt(name, pts, delimiter = ' ', newline = ';')
    
def aspectratio(pts):
    ''' Takes (xcoordinates, y coordinates) of contour and determines aspect ratio
    Newarray must be of form [x1, x2, y3 ...; y1, y2, y3 ...]'''
    newarray = np.vstack((pts[0][:,0:-1].flatten('F'), 
                          pts[1][:,0:-1].flatten('F')))
    eig = np.linalg.eig(np.cov(newarray, rowvar = True))
    return eig[0].min()/eig[0].max()

def convexhull(pts):
    conpoints = sp.spatial.ConvexHull(pts[0], pts[1])
    return conpoints 

def contouranalysis(contournumber, trialtype = 'animal'):
    '''Performs by contour analysis'''
    xcontcoord, ycontcoord = contourdata(matdata, trialtype, contournumber)
    width = np.amax(xcontcoord) - np.amin(xcontcoord)
    height = np.amax(ycontcoord) - np.amin(ycontcoord)
    aspect = aspectratio([xcontcoord, ycontcoord])
    return width, height, aspect

def ordercontouranalysis(trialtype = 'animal', 
                         orderfile = 'byanimalmetameraverage.xlsx'):
    ''' Uses contouranalysis() and getorder generator to create DataFrame
    for contours'''
    data = pd.DataFrame(columns = ['accuracy', 'width', 'height', 'aspect'])
    for contournum, contacc in getorder():
        width, height, aspect = contouranalysis(contournum, trialtype)
        data.loc[contournum] = [contacc, width, height, aspect]
    return data

if __name__ == '__main__':
    animalframe = ordercontouranalysis(trialtype = 'animal')
    metamerframe = ordercontouranalysis(trialtype = 'metamer')
    metamerframe['accuracy'] = 1 - metamerframe['accuracy']
    regtype = 'aspect'
    animalreg = linearregression(animalframe[regtype], animalframe['accuracy'])
    metamerreg = linearregression(metamerframe[regtype], metamerframe['accuracy'])
    allreg = linearregression(pd.concat([animalframe, metamerframe])[regtype],
                              pd.concat([animalframe, metamerframe])['accuracy'])
    plt.figure()
    plt.plot(animalframe[regtype], animalframe['accuracy'], 'ro', label = 'Animal')
    #plt.plot(animalframe[regtype], animalreg[2],  color = [1, 0,0, 1])
    plt.plot(metamerframe[regtype], metamerframe['accuracy'], 'bo', label = 'Metamer')
    #plt.plot(metamerframe[regtype], metamerreg[2], color = [0, 0,1, 1])
    plt.plot(pd.concat([animalframe, metamerframe])[regtype], allreg[2])
    plt.legend()