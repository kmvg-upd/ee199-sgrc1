# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:20:47 2024

@author: Carl
"""

#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' 
    Generates the random Loads, PV, and NM files
'''
from os import dup2
import sim_util

working_path = r'C:\Users\ferre\OneDrive\Documents\Thesis Files\LV Feeder'

#For generating new combinations, uncomment these.
#sim_util.gen_bus_combi(working_path, 161, 440) 2860 ata dapat
#sim_util.gen_loads(working_path)
#sim_util.gen_pv_combi(working_path, 0.7, 0.2)
#sim_util.gen_pv(working_path) 
#sim_util.pv_nm_combi(working_path, 0.7, 0.2)

# Get 55 random loads from 161 (Ausgrid).
sim_util.gen_bus_combi(working_path, 161, 1980)

# Make loads.txt for every simulation
sim_util.gen_loads(working_path)

# Get random PV for those with PV penetration
sim_util.gen_pv_combi(working_path, 1, 0.5,0.25,0.75)

# Get random NM for those with PV and NM penetration
sim_util.gen_nm_combi(working_path, 1, 0.66, 0.33)

# Make PV.txt for every simulation
sim_util.gen_pv(working_path)


# In[ ]:



