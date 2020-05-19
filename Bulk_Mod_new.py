# -*- coding: utf-8 -*-
"""
Created on Fri May  8 14:16:41 2020

@authors: shubham sinha & urja shah
"""



from mpds_client import MPDSDataRetrieval
import pandas as pd
import numpy as np
from pandas import ExcelWriter

client = MPDSDataRetrieval("sjlnBruUqQl07yZI9Hs9GhfJ0jXA0Z6FaYA27Ep2oOUHhuSz")
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
      


Bulk_Mod =  []
for x in range(len(name)):
     Bulk_M =  []
     try:
        ans = client.get_data({"formulae": name[x],'classes':'peer-reviewed', "props": "isothermal bulk modulus" })
        for i in ans:
            if i[4] == 'isothermal bulk modulus' and  i[2] == spacegroup[x]:
                Bulk_M.append(i[6]) #Appending all the Bulk Moduli values for that compound
     except:
            Bulk_M.append("NAN")
     Bulk_Mod.append(Bulk_M[:]) #Creating a list of lists which contain all different given Bulk moduli values for a particular compound

        
df = pd.DataFrame({'Bulk Modulus':Bulk_Mod})
writer = ExcelWriter('Bulk Moduli data.xlsx')
df.to_excel(writer,'Sheet2',index=False)
writer.save()
        
print(Bulk_Mod)  
