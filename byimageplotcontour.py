# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:06:04 2018
@author: David
Plot animal/metamer from contourSeginfoAllPost_20 in closedContourOrig structure
New changes: function
trialtype = animal, metamer
End bit allows plot by difficuly using rankimagebydifficulty.py  
Users order from rankimagebydifficulty.py to sort contours 
"""

import scipy.io as sio 
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.append('C:/Users/zae/Documents/summer2018')

from savefiguretopdf import savefigureloop
from rankimagebydifficulty import getorder

def loadsio(file = 'D:/contourSegInfoAllPost_20.mat'):
    return sio.loadmat(file)

def contourdata(matdata, trialtype, contournumber):
    '''
    Takes in matlab contour file, trialtype = 'animal' or = 'metamer', contournumber
    Returns onecontourx, onecontoury used to form contour plot
    '''
    if trialtype == 'animal':
        allcontours = matdata['closedContourOrig'][0]
        onecontourx = allcontours[contournumber-1][0][0][0]
        onecontoury = allcontours[contournumber-1][0][0][1]

    elif trialtype == 'metamer':
        allmetamers = matdata['contoursegMultiRotationMetamer'][0]
        onemetamer = allmetamers[contournumber-1][0]
        onemetamer = onemetamer[0] # Select which metamer to use (10 possibilities )
        onemetamer = onemetamer[0][0][0][0] 
        onecontourx = onemetamer['x'][0]
        onecontoury = onemetamer['y'][0]
    return onecontourx, onecontoury

def plotter(onecontourx, onecontoury, contournumber, accuracy, showfig = False):   
        fig = plt.figure()
        fig.suptitle('animal#: {} accuracy: {}'.format(contournumber, accuracy))
        plt.plot(onecontourx, onecontoury, '-k')
        plt.axis('square')
        if showfig == False:
            plt.close(fig)
        return fig
def contourplot(trialtype = 'animal', contournumber = 190):
    '''Quick contour plot without accuracy information
    '''
    plotter(*contourdata(loadsio(), trialtype, contournumber), 
            contournumber, accuracy = None, showfig = True)

if __name__ == '__main__':
    pass
        



