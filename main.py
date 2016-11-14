#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 14:34:35 2016

@author: dor & tal simon
"""
#test

import os  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
from scipy.io import loadmat  
import glob
import sys
from sklearn.datasets import load_iris
from sklearn import preprocessing

class Movement(object):
    
    def name(self):
        self.name

    def class_number(self):
        self.class_number
    
    def directory(self):
        self.directory
        
M0 = Movement()
M0.name='squat'
M0.class_number=0
M0.directory=r'/Users/talsimon/Desktop/Machine Learning/Squat' 

M1 = Movement()
M1.name='shoulder press'
M1.class_number=1
M1.directory=r'/Users/talsimon/Desktop/Machine Learning/SP' 

M2 = Movement()
M2.name='dead lift'
M2.class_number=2
M2.directory=r'/Users/talsimon/Desktop/Machine Learning/Deadlift' 
   
feature_num = 19   
movement_num = 3

#######################Feature Extraction Process###############


def featuresExtraction (feature_num, movement_class, path):

    allFiles = glob.glob(path + "/*")
    list_ = np.zeros((len(allFiles), feature_num))
    i = 0
    for file_ in allFiles:
        df = pd.read_csv(file_, header=None, names=['Time Stamp', 'Gyro Alpha', 'Gyro Beta', 'Gyro Gamma', 'Accel-X', 'Accel-Y', 'Accel-Z'])
        df = df.drop(df.index[[0,1]])
        df = df.drop('Time Stamp', axis=1)
        df = preprocessing.normalize(df)
        temp = pd.DataFrame(df)
        list_[i, 0:6] = temp.mean().reshape(1,6)
        list_[i, 6:12] = temp.std().reshape(1,6)
        list_[i, 12:18] = temp.median().reshape(1,6)
        list_[i, feature_num - 1] = movement_class
        i = i + 1    
    np.savetxt('SquatProcessed', list_,delimiter=',')
    return [path]

###############################################################

j=0
for j in movement_num: 
    featuresExtraction(j,j,r'/Users/dorsimon/ML_Project/Data Set/Squat')  
    j=j+1
