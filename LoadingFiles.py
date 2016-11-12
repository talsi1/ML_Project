#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 14:34:35 2016

@author: talsimon
"""
import os  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
from scipy.io import loadmat  
import glob
import sys
from sklearn.datasets import load_iris
from sklearn import preprocessing

feature_num = 19
squatClass = 0 
spClass = 1 
dlClass = 2

######################Processing Squat#########################

path =r'/Users/talsimon/Desktop/Machine Learning/Squat' # use your path
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
    list_[i, feature_num - 1] = squatClass
    i = i + 1 
    
np.savetxt('SquatProcessed', list_,delimiter=',')

######################Processing SP#########################

path =r'/Users/talsimon/Desktop/Machine Learning/SP' # use your path
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
    list_[i, feature_num - 1] = spClass
    i = i + 1 
    

np.savetxt('SP-Processed', list_,delimiter=',')


######################Processing Deadlift#########################


path =r'/Users/talsimon/Desktop/Machine Learning/Deadlift' # use your path
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
    list_[i, feature_num - 1] = dlClass
    i = i + 1 
    

np.savetxt('Deadlift-Processed', list_,delimiter=',')


path = os.getcwd() + '/SquatProcessed'
squat_data = pd.read_csv(path, header=None, names=['Gyro Alpha Mean', 'Gyro Beta Mean', 'Gyro Gamma Mean', 'Accel-X Mean', 'Accel-Y Mean', 'Accel-Z Mean', 'Gyro Alpha STD', 'Gyro Beta STD', 'Gyro Gamma STD', 'Accel-X STD', 'Accel-Y STD', 'Accel-Z STD', 'Gyro Alpha MED', 'Gyro Beta MED', 'Gyro Gamma MED', 'Accel-X MED', 'Accel-Y MED', 'Accel-Z MED', 'Label'])
sq = pd.DataFrame(squat_data)

path = os.getcwd() + '/SP-Processed'
sp_data = pd.read_csv(path, header=None, names=['Gyro Alpha Mean', 'Gyro Beta Mean', 'Gyro Gamma Mean', 'Accel-X Mean', 'Accel-Y Mean', 'Accel-Z Mean', 'Gyro Alpha STD', 'Gyro Beta STD', 'Gyro Gamma STD', 'Accel-X STD', 'Accel-Y STD', 'Accel-Z STD', 'Gyro Alpha MED', 'Gyro Beta MED', 'Gyro Gamma MED', 'Accel-X MED', 'Accel-Y MED', 'Accel-Z MED', 'Label'])
sp = pd.DataFrame(sp_data)

path = os.getcwd() + '/Deadlift-Processed'
dl_data = pd.read_csv(path, header=None, names=['Gyro Alpha Mean', 'Gyro Beta Mean', 'Gyro Gamma Mean', 'Accel-X Mean', 'Accel-Y Mean', 'Accel-Z Mean', 'Gyro Alpha STD', 'Gyro Beta STD', 'Gyro Gamma STD', 'Accel-X STD', 'Accel-Y STD', 'Accel-Z STD', 'Gyro Alpha MED', 'Gyro Beta MED', 'Gyro Gamma MED', 'Accel-X MED', 'Accel-Y MED', 'Accel-Z MED', 'Label'])
dl = pd.DataFrame(dl_data) 

X = pd.DataFrame()       
X = X.append(sq)
X = X.append(sp)
X = X.append(dl)



X = np.matrix(X.values)
np.random.shuffle(X)

#y = pd.DataFrame(X)
#y = y.drop(y.columns[:feature_num - 1], axis=1)
#y = np.matrix(y.values)

np.savetxt('data_set_full', X,delimiter=',')

 