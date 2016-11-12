#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 21:16:53 2016

@author: talsimon
"""

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
#import seaborn as sb  
from scipy.io import loadmat  
from sklearn import svm  

def gaussian_kernel(x1, x2, sigma):  
    return np.exp(-(np.sum((x1 - x2) ** 2) / (2 * (sigma ** 2))))


path = '/Users/talsimon/data_set_full'
raw_data = pd.read_csv(path, header=None, names=['Gyro Alpha Mean', 'Gyro Beta Mean', 'Gyro Gamma Mean', 'Accel-X Mean', 'Accel-Y Mean', 'Accel-Z Mean', 'Gyro Alpha STD', 'Gyro Beta STD', 'Gyro Gamma STD', 'Accel-X STD', 'Accel-Y STD', 'Accel-Z STD', 'Gyro Alpha MED', 'Gyro Beta MED', 'Gyro Gamma MED', 'Accel-X MED', 'Accel-Y MED', 'Accel-Z MED', 'Label'])

# append a ones column to the front of the data set
raw_data.insert(0, 'Ones', 1)

# set X (training data) and y (target variable)
cols = raw_data.shape[1]  
X = raw_data.iloc[:200,0:cols-1]  
y = raw_data.iloc[:200,cols-1:cols]
Xval = raw_data.iloc[200:290,0:cols-1]
yval = raw_data.iloc[200:290,cols-1:cols]
test = raw_data.iloc[294,0:cols-1]
test_y = raw_data.iloc[294,cols-1:cols]


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


