# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:37:44 2018
@author: David
Performs analysis on excel generated by byimagegenerateexcel
First analysis: Animal# vs mean accuracy of trials with that animal


THIS IS AN OLD VERSION. GO TO rankimagebydifficulty.py 
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = 'C:/Users/zae/Documents/summer2018/ReplicationData/animalmetamer.xlsx'
excel = pd.ExcelFile(file)
data = excel.parse('data')
maxanimal = data['animal#'].max()
                 
'''
Average by animal number
'''

#animalframe = pd.DataFrame(columns = ['animalnumber', 'animalaverages'])
#allanimalaverage = []
#for animalnumber in range(1, maxanimal+1):
#    animaldata = data[data['animal#'] == animalnumber]
#    animalaverage = animaldata['correct'].mean()
#    allanimalaverage.append(animalaverage)
#    animalframe.loc[animalnumber] = [animalnumber, animalaverage]
#
#animalframe = animalframe.sort_values(by = 'animalaverages', ascending = False)
#writer = pd.ExcelWriter('animalnumberaverage.xlsx', engine = 'xlsxwriter')
#animalframe.to_excel(writer, sheet_name = 'data')
#writer.save()

'''
Split trial by animal or metamer. Than combine mirror animal data and average
Than show top20 and bottom20 in byimageplotcontour.py
'''
animalframe = data[data['AnimalorMetamer'] == 1] # 1 is animal
metamerframe = data[data['AnimalorMetamer'] == 0] # 0 is metamer

animalaverages = pd.DataFrame(columns = ['animalnumber', 'animalaverages'])
for animalnumber in range(1, maxanimal+1, 2):
    animaldata = animalframe[animalframe['animal#'] == animalnumber]
    animaldata = animaldata.append(animalframe[animalframe['animal#'] == animalnumber +1])
    animalaverage = animaldata['correct'].mean()
    animalaverages.loc[animalnumber] = [animalnumber, animalaverage]


metameraverages = pd.DataFrame(columns = ['metamernumber', 'metameraverages'])
for metamernumber in range(1, maxanimal+1):
    metamerdata = metamerframe[metamerframe['animal#'] == metamernumber]
    metameraverage = metamerdata['correct'].mean()
    metameraverages.loc[metamernumber] = [metamernumber, metameraverage]

animalaverages = animalaverages.sort_values(by = 'animalaverages', ascending = False)
metameraverages = metameraverages.sort_values(by = 'metameraverages', ascending = False)

writer = pd.ExcelWriter('animalmetameraverages.xlsx', engine = 'xlsxwriter')
animalaverages.to_excel(writer, sheet_name = 'animalnumbers')
metameraverages.to_excel(writer, sheet_name = 'metamernumbers')
writer.save() 