# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 22:13:37 2016

@author: dorsimon
"""


'''
Reads in data over a serial connection and plots the results live. Before closing, the data is saved to a .txt file.
'''
import serial
import matplotlib.pyplot as plt
import numpy as np
#import datetime
#import win32com.client

i=0
j=0
#connected = True

#finds COM port that the Arduino is on (assumes only one Arduino is connected)

print('1')

s = serial.Serial(port='/dev/cu.wchusbserial1420', baudrate=9600)

plt.ion()                    #sets plot to animation mode
length = 80                  #determines length of data taking session (in data points)
acc_x = [0]*length               #create empty variable of length of test
acc_y = [0]*length
acc_z = [0]*length
gy_x = [0]*length               
gy_y = [0]*length
gy_z = [0]*length

print('2')


acc_xline, = plt.plot(acc_x)         #sets up future lines to be modified
acc_yline, = plt.plot(acc_y)
acc_zline, = plt.plot(acc_z)
gy_xline, = plt.plot(gy_x)         
gy_yline, = plt.plot(gy_y)
gy_zline, = plt.plot(gy_z)

plt.ylim(-8000,300)        #sets the y axis limits
for j in range(5):
    for i in range(length):     #while you are taking data
        print('3')    
        data = s.readline()    #reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
        print('4')
        i=i+1
        sep = data.split()      #splits string into a list at the tabs
        print('5')
        print (sep)
        print('6')
        acc_x.append(int(sep[0]))   #add new value as int to current list
        acc_y.append(int(sep[1]))
        acc_z.append(int(sep[2]))
        gy_x.append(int(sep[3]))   
        gy_y.append(int(sep[4]))
        gy_z.append(int(sep[5]))
        
        print('7')
        del acc_x[0]
        del acc_y[0]
        del acc_z[0]
        del gy_x[0]
        del gy_y[0]
        del gy_z[0]
        
        acc_xline.set_xdata(np.arange(len(acc_x))) #sets xdata to new list length
        acc_yline.set_xdata(np.arange(len(acc_y)))
        acc_zline.set_xdata(np.arange(len(acc_z)))
        gy_xline.set_xdata(np.arange(len(gy_x))) 
        gy_yline.set_xdata(np.arange(len(gy_y)))
        gy_zline.set_xdata(np.arange(len(gy_z)))
        
        #print('9')
        acc_xline.set_ydata(acc_x)                 #sets ydata to new list
        acc_yline.set_ydata(acc_y)
        acc_zline.set_ydata(acc_z)
        gy_xline.set_ydata(gy_x)                 
        gy_yline.set_ydata(gy_y)
        gy_zline.set_ydata(gy_z)
        
        #print('10')
        plt.draw()                         #draws new plot
        #print('11')
    
    rows = list(zip(acc_x, acc_y, acc_z, gy_x, gy_y, gy_z))               #combines lists together
    #print(rows)
    #print('12')
    
    row_arr = np.array(rows)               #creates array from list
    print(row_arr)
    #print('13')
    
    #savetxt_compact('/Users/dorsimon/Desktop/test_radio2.txt', row_arr, fmt='%.4f')
    
    with open('/Users/dorsimon/Desktop/Workout.csv','ab') as f_handle: #ab mode enables to append the new values, a for append, b for binary values
        np.savetxt(f_handle,row_arr)
    
    
    #old writing options
    #np.savetxt('/Users/dorsimon/Desktop/Wourout.txt', row_arr) #save data in file (load w/np.loadtxt())
    #np.savetxt('/Users/dorsimon/Desktop/Wourout_' + str(datetime.datetime.now().strftime('%d%mU%H%M%S')) + '.txt', row_arr) #save data in file (load w/np.loadtxt())
    
    #print('14')
    
    #s.close() #closes serial connection (very important to do this! if you have an error partway through the code, type this into the cmd line to close the connection)
    print('15')

