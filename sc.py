#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:22:31 2020

@author: urjashah
"""


from pymatgen import MPRester
m = MPRester("mhZFpeEy6dioJg19")
import numpy as np

import pandas as pd
from pandas import ExcelWriter

file = pd.read_csv('a_assay_Petretto.txt',sep="\t",header=None)
file1= file[0]
file1.pop(0)

#name=m.query(criteria={"task_id":"mp-10044"},properties=["pretty_formula"])
file1=list(file1)
name=[]
for i in range(len(file1)):
    data=m.query(criteria={"task_id":file1[i]},properties=["pretty_formula"])
    name.append(data)
const=[]
for i in range(len(file1)):
    data=m.query(criteria={"task_id":file1[i]},properties=["phonon_dispersion"])
    const.append(data)
df = pd.DataFrame({'Formula':name})
df1=pd.DataFrame({'MP ID':file1})
df2=pd.DataFrame({'Phonon Dispersion':const})
writer=ExcelWriter('pd_sc_f.xlsx')
df.to_excel(writer,'Sheet1',index=False,startcol=0)
df1.to_excel(writer,'Sheet1',index=False,startcol=1)
df2.to_excel(writer,'Sheet1',index=False,startcol=2)
writer.save()

    
