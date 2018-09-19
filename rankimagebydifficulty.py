# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:11:06 2018
@author: David
Uses data from byimagegenerateexcel.py -> animalmetamer.xlsx
animalmetamer.xlsx is excel with animal number and subjects response
This file sorts animal by accuracy score like byimageanalysis but:
    does not combine mirror image (Has it as an option)

Notes:
    Seperates animal and metamer number: animal ranked by just animal performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def rankimage(file = ' animalmetamer.xlsx', animalmirrorcombine = False, 
              metamer = True, savefile = 'animalmetameraverage.xlsx'):
    ''' Uses data from byimagegenerateexcel.py -> animalmetamer.xlsx
    animalmirrorcombine = True combines mirror animal data
    metamer = True uses metamer data as well
    '''
    excel = pd.ExcelFile(file)
    data = excel.parse('data')
    maxanimal = data['animal#'].max()
    animalframe = data[data['AnimalorMetamer'] == 1] # 1 is animal
    animalaverages = pd.DataFrame(columns = ['animalnumber', 'animalaverages'])
    
    for animalnumber in range(1, maxanimal+1, animalmirrorcombine+1):
        animaldata = animalframe[animalframe['animal#'] == animalnumber]
        animaldata = animaldata.append(animalframe[animalframe['animal#'] == animalnumber +1])
        animalaverage = animaldata['correct'].mean()
        animalaverages.loc[animalnumber] = [animalnumber, animalaverage]
    animalaverages = animalaverages.sort_values(by = 'animalaverages', ascending = False)
    
    if metamer == True:
        metamerframe = data[data['AnimalorMetamer'] == 0] # 0 is metamer
        metameraverages = pd.DataFrame(columns = ['metamernumber', 'metameraverages'])
        for metamernumber in range(1, maxanimal+1):
            metamerdata = metamerframe[metamerframe['animal#'] == metamernumber]
            metameraverage = metamerdata['correct'].mean()
            metameraverages.loc[metamernumber] = [metamernumber, metameraverage]
        metameraverages = metameraverages.sort_values(by = 'metameraverages', ascending = False)
    
    writer = pd.ExcelWriter(savefile, engine = 'xlsxwriter')
    animalaverages.to_excel(writer, sheet_name = 'animalnumbers')
    if metamer == True:
        metameraverages.to_excel(writer, sheet_name = 'metamernumbers')
    writer.save() 

def getorder(orderfile = 'byanimalmetameraverage.xlsx', trialtype = 'animal'):
    '''returns ordered contournumber, average tuple in generator object
    Order from excel produced by rankimage() 
    '''
    orderdata = pd.read_excel(orderfile, sheet_name = trialtype+'numbers')
    for contournumber in list(orderdata[trialtype+'number']):
        yield (contournumber, round(orderdata.loc[contournumber][trialtype+'averages'], 3))

#if __name__ == '__main__':
#    file = 'C:/Users/zae/Documents/summer2018/ReplicationData/animalmetamer.xlsx'
#    rankimage(file, animalmirrorcombine = False, metamer = True, savefile = 'byanimalmetameraverage.xlsx')
        