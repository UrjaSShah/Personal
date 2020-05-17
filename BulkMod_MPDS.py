# -*- coding: utf-8 -*-
"""
Created on Fri May  8 14:16:41 2020

@authors: shubham sinha & urja shah
"""
#This code is used to extract superconducting Tc and Bulk Moduli data from
#the MPDS database using the API information. The code extracts the info
#for all the compounds from a given list and extracts the necessary info
#That is then added to an excel sheet and saved. The code uses a sleep
#function to give the code 1 second before feeding in the next compound 
#into the database so as to not overwork the system.

#import all necessary python packages
from mpds_client import MPDSDataRetrieval
import pandas as pd
import numpy as np
from pandas import ExcelWriter
import time
# feed in personalized API KEY
client = MPDSDataRetrieval(" API KEY")
sc_datafile=pd.read_excel(r'Bulk Moduli.xlsx') #This reads the excel file containing name of compounds and their spacegroup as obtained from MP
# The following lines convert panda dataframe type to numpy array
name = pd.DataFrame(sc_datafile,columns=['Compound'])
name = name.values.tolist()
name = np.asarray(name)
name = np.concatenate(name,axis=0)
spacegroup = pd.DataFrame(sc_datafile,columns=['Space group'])
spacegroup = spacegroup.values.tolist()
spacegroup = np.asarray(spacegroup)
spacegroup = np.concatenate(spacegroup,axis=0)
answer=[]
Tc=[]
Tc_actual=[]
formula=[]

print(name)
print(spacegroup)
#Extracting Superconducting Tc
# To extract the Tc value from a given set of properties for the compound
#it must reach the criteria of having 'superconducting transition temperature'
#otherwise the temperature is not associated with the quantity we want
#and for such compounds the results would show nan

'''
for x in range(len(name)):
     T =  []
     try:
        ans = client.get_data({"formulae": name[x],'classes':'peer-reviewed', "props": "superconductivity" })
        for i in ans:
            if i[4] == 'superconducting transition temperature' and  i[2] == spacegroup[x]: #checking the spacegroup on MPDS and MP match
                T.append(i[6]) #Appending all the Tc values for that compound
     except:
           T.append("NAN") 
     Tc.append(T[:]) #Creating a list of lists which contain all different given Transition Temperature values for a particular compound

#Converting Tc into panda dataframe      
df = pd.DataFrame({'Transition Temp':Tc})
#Writing to an excel file
writer = ExcelWriter('temp.xlsx')
#excel sheet
df.to_excel(writer,'Sheet1',index=False)
#saving the excel file
writer.save()
print(Tc) 
'''   

#Extracting the isothermal bulk modulus data in a similar manner
Bulk_Mod =  []
for x in range(len(name)):
     Bulk_M =  []
     try:
        time.sleep(1)
        ans = client.get_data({"formulae": name[x],'classes':'peer-reviewed', "props": "isothermal bulk modulus" })
        for i in ans:
            if i[4] == 'isothermal bulk modulus' and  i[2] == spacegroup[x]:
                Bulk_M.append(i[6]) #Appending all the Bulk Moduli values for that compound
     except:
            Bulk_M.append("NAN")
     Bulk_Mod.append(Bulk_M[:]) #Creating a list of lists which contain all different given Bulk moduli values for a particular compound

 #Saving it in a given excel sheet       
df = pd.DataFrame({'Bulk Modulus':Bulk_Mod})
writer = ExcelWriter('temp3.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()
        
print(Bulk_Mod )  
