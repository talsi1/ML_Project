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
import glob
import sys
from sklearn.datasets import load_iris
from sklearn import preprocessing
import scipy as sp
from scipy import signal
from scipy import stats
from sklearn import svm  


#######################Feature Extraction Process###############


def featuresExtraction (movement_class, path):
    feature_num = 34
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
        list_[i, 18:19] = np.fft.fftn(temp).max()
        list_[i, 19:20] = np.fft.fftn(temp).min()
        list_[i, 20:26] = sp.stats.skew(np.fft.fftn(temp)).reshape(1,6)
        list_[i, 26:32] = sp.stats.kurtosis(np.fft.fftn(temp)).reshape(1,6)
        list_[i, 33] = sp.stats.iqr(temp)
        list_[i, feature_num - 1] = movement_class
        i = i + 1    

    return list_

###############################################################


X_squat = pd.DataFrame(featuresExtraction(0, r'/Users/talsimon/Desktop/Machine Learning/Squat'))  
X_sp = pd.DataFrame(featuresExtraction(1, r'/Users/talsimon/Desktop/Machine Learning/SP'))
X_dl = pd.DataFrame(featuresExtraction(2, r'/Users/talsimon/Desktop/Machine Learning/Deadlift'))

X = pd.DataFrame()       
X = X.append(X_squat)
X = X.append(X_sp)
X = X.append(X_dl)

X = np.matrix(X.values)
np.random.shuffle(X)

raw_y = pd.DataFrame(X)
raw_y = raw_y.drop(raw_y.columns[:33], axis=1)

#y = np.matrix(y.values)

raw_data_x = pd.DataFrame(X)
raw_data_x = raw_data_x.drop(raw_data_x.columns[33], axis=1)
#raw_data_y = pd.DataFrame(y)

# append a ones column to the front of the data set
raw_data_x.insert(0, 'Ones', 1)

# set X (training data) and y (target variable)
cols = raw_data_x.shape[1]  
X = raw_data_x.iloc[:200,0:cols-1]  
y = raw_y.iloc[:200,0]
Xval = raw_data_x.iloc[200:290,0:cols-1]
yval = raw_y.iloc[200:290,0]


C_values = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100]  
gamma_values = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100]

best_score = 0  
best_params = {'C': None, 'gamma': None}

for C in C_values:  
    for gamma in gamma_values:
        svc = svm.SVC(C=C, gamma=gamma)
        svc.fit(X, y)
        score = svc.score(Xval, yval)

        if score > best_score:
            best_score = score
            best_params['C'] = C
            best_params['gamma'] = gamma


