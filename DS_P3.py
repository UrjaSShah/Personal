#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:59:25 2022

@author: urjashah
"""
#importing necessary packages
import numpy as np
import matplotlib.pyplot as plt

#importing the data text file and converting columns into arrays
#remember to change directory to wherever the data file is saved

Data_file = np.loadtxt("C:\\User\urjashah\Downloads\IceCube_Data_Project3.txt")
Time = Data_file[0]
print(Time)