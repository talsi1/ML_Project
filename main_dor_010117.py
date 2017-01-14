#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 14:34:35 2016

@author: dor & tal simon
"""
#test

import os as os
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import glob
import sys
import time
from sklearn.datasets import load_iris
from sklearn import preprocessing
import scipy as sp
from scipy import signal
from scipy import stats
from sklearn import svm  


#######################Feature Extraction Process###############

def featuresExtraction (movement_class, path, feature_num):
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
        #list_[i, 18:19] = np.fft.fftn(temp).max()
        #list_[i, 18:19] = preprocessing.normalize(list_[i, 18:19])
        #list_[i, 19:20] = np.fft.fftn(temp).min()
        #list_[i, 20:26] = sp.stats.skew(np.fft.fftn(temp)).reshape(1,6)
        #list_[i, 26:32] = sp.stats.kurtosis(np.fft.fftn(temp)).reshape(1,6)
        #list_[i, 33] = sp.stats.iqr(temp)
        list_[i, feature_num - 1] = movement_class
        i = i + 1    

    return list_
    
def featuresExtraction2 (movement_class, path, feature_num):
    df = pd.read_csv(path, header=None, names=['Time Stamp', 'Gyro Alpha', 'Gyro Beta', 'Gyro Gamma', 'Accel-X', 'Accel-Y', 'Accel-Z'])
    df = df.drop('Time Stamp', axis=1)
    df = df.tail(85)
    list_ = np.zeros((1, feature_num))
    df = preprocessing.normalize(df)
    temp = pd.DataFrame(df)
    
    list_[0, 0:6] = temp.mean().reshape(1,6)
    list_[0, 6:12] = temp.std().reshape(1,6)
    list_[0, 12:18] = temp.median().reshape(1,6)
    #list_[0, 18:19] = np.fft.fftn(temp).max()
    #list_[i, 18:19] = preprocessing.normalize(list_[i, 18:19])
    #list_[i, 19:20] = np.fft.fftn(temp).min()
    #list_[i, 20:26] = sp.stats.skew(np.fft.fftn(temp)).reshape(1,6)
    #list_[i, 26:32] = sp.stats.kurtosis(np.fft.fftn(temp)).reshape(1,6)
    #list_[i, 33] = sp.stats.iqr(temp)
    list_[0, feature_num - 1] = movement_class

    return list_

###############################################################

    
feature_num = 19
print('1')
#X_none = pd.DataFrame(featuresExtraction(0, r'/Users/dorsimon/ML_Project/Data Set/None', feature_num))  
X_squat = pd.DataFrame(featuresExtraction(1, r'/Users/dorsimon/ML_Project/Data Set/Squat', feature_num))  
X_sp = pd.DataFrame(featuresExtraction(2, r'/Users/dorsimon/ML_Project/Data Set/SP', feature_num))
X_dl = pd.DataFrame(featuresExtraction(3, r'/Users/dorsimon/ML_Project/Data Set/Deadlift', feature_num))


X = pd.DataFrame()       
X = X.append(X_none)
X = X.append(X_squat)
X = X.append(X_sp)
X = X.append(X_dl)

X = np.matrix(X.values)
np.random.shuffle(X)

# append a ones column to the front of the data set
raw_data_x = pd.DataFrame(X)

raw_data_x.insert(0, 'Ones', 1)

# set X (training data) and y (target variable)
cols = raw_data_x.shape[1]


X = np.matrix(raw_data_x.iloc[:300,:cols-1].values)  
Xval = np.matrix(raw_data_x.iloc[300:390,:cols-1].values)


y = raw_data_x.iloc[:300,cols-1:cols]
yval = raw_data_x.iloc[300:390,cols-1:cols]

y = np.array(y.values).ravel()
yval = np.array(yval.values).ravel()


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

path = r'/Users/dorsimon/Desktop/Workout.csv'
while True:
    prediction = pd.DataFrame(featuresExtraction2(0, path, feature_num))  
    prediction.insert(0, "One", 1)
    X_stream = np.matrix(prediction.iloc[:,:cols-1].values)
    print(svc.predict(X_stream))
    np.savetxt(r'/Users/dorsimon/ML_Project/data-gathering/classification', svc.predict(X_stream), fmt='%i')
    time.sleep(1.5)

    