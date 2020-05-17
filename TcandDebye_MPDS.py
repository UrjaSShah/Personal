# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:37:46 2020

@author: j.destefano
"""

# This code is used to extract Tc and Debye temperatures from a list of 
#compounds in the MPDS database. It created an average for compound entries
#with more than 1 result for Tc and Debye and saves the respective arrays in
#excel sheets. An important function of sleep time is used to prevent the 
#dabase from being overloaded and give it 1 second before feeding in the 
#nect query. 
from mpds_client import MPDSDataRetrieval
import numpy as np
import statistics
import time
import pandas as pd
from pandas import ExcelWriter
client = MPDSDataRetrieval("API KEY")

import xlrd
# this snippet imports the spreadsheet into Python
workbook = xlrd.open_workbook('Bulk Moduli Data.xlsx')
sheet = workbook.sheet_by_name('Sheet1')
compound_list = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

entries = len(compound_list)

# this redefinition of compound is because I want a list, not a list of lists
compound = []
entries = len(compound_list)
for x in range(0, entries):
    compound.append(compound_list[x][0])

# this initializes the arrays
space_group = []
debye = []
tc = []
debye_check = []
tc_check = []
dictionary = {"props": "Debye temperature", "classes": "peer-reviewed"}

for y in range(0, entries):
    # this command updates the dictionary with the new compound each time through the loop
    time.sleep(1)
    dictionary.update([('formulae', compound[y])])
    # I used a try command here just in case there was an issue with my list of compounds and one of them didn't have a listed Debye temperature
    try:
        # adds the space group from each entry to a list
        database = client.get_data(dictionary)
        hits = len(database)
        space_group.append(database[0][2])
        cur_debye = []
        for z in range(0,hits):
            # THIS LINE IS IMPORTANT: if you don't check that the fourth positiion is what you're looking for, you may get weird results. In this case, without this line I was stripping both Debye and Einstein temperatueres
            if database[z][4] == 'Debye temperature':
                cur_debye.append(database[z][6])
        debye_entries = len(cur_debye)
        # this if statement just allows the skipping of getting the average is there is only one compound
        if debye_entries == 1:
            debye.append(database[z][6])
            debye_check.append(' ')
        else:
            debye_average = statistics.mean(cur_debye)
            debye_high = max(cur_debye)
            debye_low = min(cur_debye)
            debye_std = statistics.stdev(cur_debye)
            formula = debye_std/debye_average
            debye.append("%g entries from %g - %g. Average of %g" % (debye_entries, debye_low, debye_high, debye_average))
            debye_check.append(formula)
    except:
        debye.append("No Debye T")
        debye_check.append("Ignore this entry")
    
dictionary = {"props": "superconducting transition temperature", "classes": "peer-reviewed"}
'''
# this entiere for loop just redoes what happened with the Debye temperature, but with the critical temperature
for a in range(0, entries):
    time.sleep(0.1)
    dictionary.update([('formulae', compound[a])])
    # this try is due to the fact that I started search with Debye temperatures, so not all will have a Tc listed
    try:
        database = client.get_data(dictionary)
        hits = len(database)
        cur_tc = []
        for b in range(0,hits):
            if database[b][4] == 'superconducting transition temperature':
                cur_tc.append(database[b][6])
        tc_entries = len(cur_tc)
        if tc_entries == 1:
            tc.append(database[b][6])
            tc_check.append(' ')
        else:
            tc_average = statistics.mean(cur_tc)
            tc_high = max(cur_tc)
            tc_low = min(cur_tc)
            tc_std = statistics.stdev(cur_tc)
            formula = tc_std/tc_average
            tc.append("%g entries from %g - %g. Average of %g" % (tc_entries, tc_low, tc_high, tc_average))
            tc_check.append(formula)
    except:
        tc.append("No Tc")
        tc_check.append("Ignore this entry")
 '''       
# I turned all of these into arrays so I could concatonate them and export to a spreadsheet easily    
compound_array = np.array(compound)
space_group_array = np.array(space_group)
#tc_array = np.array(tc)
#tc_check_array = np.array(tc_check)
debye_array = np.array(debye)
debye_check_array = np.array(debye_check)

#result = np.c_[compound_array, space_group_array, tc_array, tc_check_array, debye_array, debye_check_array]

df = pd.DataFrame({'Debye':debye_array})
#df = pd.DataFrame({'Tc':tc_array})
writer = ExcelWriter('Bulk Moduli Data.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()

#print(tc_array)
print(debye_array)
