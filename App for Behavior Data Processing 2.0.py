# -*- coding: utf-8 -*-
"""
Last version created on December 11th, 2023

@author: marianna cecyn
"""

## Created by Marianna Cecyn 
## github: https://github.com/mariannacecyn 
## orcid: https://orcid.org/0000-0002-4995-7482
## linkedin: https://www.linkedin.com/in/mariannacecyn 


import pandas as pd
import numpy as np
import os
#import openpyxl 


    
def MatrizTransicaoCont(array):
    #this function creates an counting matrix of transitions for each animal
    matrixcont = pd.crosstab(
        pd.Series(array[:-1], name='from'), #row
        pd.Series(array[1:], name='to'), #column
        margins=True)
    return matrixcont


def MatrizTransicaoProb(array):
    #this function creates an Matrix of Markov for each animal  
    matrixprob = pd.crosstab(
        pd.Series(array[:-1], name='from'), ##row
        pd.Series(array[1:], name='to'), ##column
        normalize="columns",
        margins=True)
    return matrixprob
    

def Frequencias(array):
    #this fuction counts the frequencies of Boris ethogram behaviors
    ##### KEY POINT OF ATTENCION:
    #It is very important to check that the dictionary 
    #has exactly the same behavior as your ethogram 
    #and that the spelling is exactly the same with upper and lower case letters, 
    #spacing, special characters, etc. 
    i=0
    #epm (comment if you don't use it)
    Frequencies = {'Rearing close': 0, 'Stretching close': 0, 'Head out close': 0, 'Grooming close': 0, 'Sniffing close': 0, 'Walking close': 0, 'Rearing open': 0, 'Head dipping open': 0, 'Grooming open': 0, 'Sniffing open': 0, 'Walking open': 0}
    #ldb (comment if you don't use it)
    Frequencies = {'Rearing': 0, 'Stretching': 0, 'Head out': 0, 'Grooming': 0, 'Sniffing': 0, 'Walking': 0, 'Light side entry':0, 'Dark side entry': 0} 
    while i < array.size:  
      Key = array[i] 
     
      if Key in Frequencies:
          Frequencies[Key] = Frequencies[Key] + 1 
      else:
          Frequencies[Key] = 1 
      i = i+1

    dfFreq = pd.DataFrame.from_dict(Frequencies, orient ='index') 
    dfFreqt = dfFreq.T
    return dfFreqt

def Probabilidades(array):
    #this function created the State Vector for Markov Chain 
    Probabilities = {}
    i=1
    while i < contBehavior:
        Key = array[i] 
        if Key in Probabilities:
            Probabilities[Key] = Probabilities[Key] + 1 
        else:
            Probabilities[Key] = 1 
        i = i+1
    for key in Probabilities:
        Probabilities[key] /= contBehavior
    dfProb = pd.DataFrame.from_dict(Probabilities, orient ='index') 
    return dfProb
    
           
def Transicoes(array):
    #this fuction creates an dictionary with all count transitions, 
    #more easily manipulated in Excel and exported to statistical software 
    Transitions = {} 
    i=1
    while i < contBehavior:
        
      Key = str(array[i-1]) + " - " + str(array[i]) 
      if Key in Transitions:
          Transitions[Key] = Transitions[Key] + 1 
      else:
          Transitions[Key] = 1 
      i = i+1
    
    dfTrans = pd.DataFrame.from_dict(Transitions, orient ='index')
    dfTranst = dfTrans.T
    return dfTranst

def TransicoesProb(array):
    #this fuction creates an dictionary with all probability of transitions, 
    #more easily manipulated in Excel and exported to statistical software 
    TransitionsProb = {} 
    Transitions = {} 
    i=1
    while i < contBehavior:
        
      Key = str(array[i-1]) + " - " + str(array[i]) 
      if Key in Transitions:
          Transitions[Key] = Transitions[Key] + 1 
      else:
          Transitions[Key] = 1 
      i = i+1
    totaltrans = len(Transitions)
    
    x = 0 
    while x < totaltrans: 
        for key in TransitionsProb:
            TransitionsProb[key] = Transitions[key]/totaltrans
    
    dfTransProb = pd.DataFrame.from_dict(TransitionsProb, orient ='index')
    dfTranstProb = dfTransProb.T
    return dfTranstProb

#INICIANDO...

print("\n================================")
print("App for Behavior Data Processing \n Created by Marianna Cecyn \n Please cite  \n github: https://github.com/mariannacecyn  \n orcid: https://orcid.org/0000-0002-4995-7482 \n linkedin: https://www.linkedin.com/in/mariannacecyn")
print("\n================================")   
folder = input("Paste here the full path of the data folder you would like to process: ")
path = folder
files = os.listdir(path)
files_xlsx = [path + '/' + f for f in files if f[-5:] == '.xlsx' ]
animals = [a[-15:-5] for a in files if a[-5:] == '.xlsx'] 
#here you must change a string depending your file name lenght
print("\n================================")
datasubj = pd.DataFrame(animals)
databaseBehaviors = pd.DataFrame()
databaseTrans = pd.DataFrame()

for f in files_xlsx:
          
    df_original = pd.read_excel(f) 
    arr = df_original["Behavior"].values 
    #wb = pd.ExcelWriter(folder + '/pythonBDPV-' + f[-10:]) #this line is use if you want one excel file for each animal
        
    for i in arr:
        if i == "Open arm":   
            arr = np.delete(arr, np.where(arr == i))
        if i == "Close arm":
            arr = np.delete(arr, np.where(arr == i))
        if i == "Start of experiment":
            arr = np.delete(arr, np.where(arr == i))
        if i == "End of experiment":
            arr = np.delete(arr, np.where(arr == i))
        if i == "Start of test":
            arr = np.delete(arr, np.where(arr == i))
        if i == "End of test":
            arr = np.delete(arr, np.where(arr == i))
        if i == "Center cross":
            arr = np.delete(arr, np.where(arr == i))
        if i == "Not moving":
            arr = np.delete(arr, np.where(arr == i))
        else: arr = arr

        
    contBehavior = np.size(arr)
    FreqBehaviors = Frequencias(arr)
    databaseBehaviors = databaseBehaviors.append(FreqBehaviors)  

    
    #TransCont = Transicoes(arr)
    #databaseTrans = databaseTrans.append(TransCont)
databaseBehaviors.insert(0, 'Animal', animals)
#print(databaseBehaviors)   
#print(database)
#print(databasecomplete)
    
wb = pd.ExcelWriter(folder + '/alldataexperiment.xlsx') #you can choose the name of output file
databaseBehaviors.to_excel(wb)   
wb.save()
      

    
    ##### for individual output
    #df_original.to_excel(wb, sheet_name='Boris')
    #pd.DataFrame(arr).to_excel(wb, sheet_name='SeqBehaviors')
    #Frequencias(arr).to_excel(wb, sheet_name='FreqBehaviors')
    #Probabilidades(arr).to_excel(wb, sheet_name='ProbBehaviors')
    #Transicoes(arr).to_excel(wb, sheet_name='TransCont')
    #MatrizTransicaoCont(arr).to_excel(wb, sheet_name='ContMatrix')
    #MatrizTransicaoProb(arr).to_excel(wb, sheet_name='ProbMatrix') 
    #wb.save() 


   


