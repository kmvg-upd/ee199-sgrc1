#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' 
    Iterative OpenDSS simulation for the whole dataset through COM.
'''
import win32com.client
import os
import shutil


# In[2]:


working_path = r"C:\Users\ferre\OneDrive\Documents\Thesis Files\LV Feeder\CM1"


# In[3]:


dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
dssText = dssObj.Text
dssCircuit = dssObj.ActiveCircuit
dssSolution = dssCircuit.Solution
dssElem = dssCircuit.ActiveCktElement
dssBus = dssCircuit.ActiveBus


# In[4]:


# Iterate through buscombi.
with open(working_path + r"\BusCombi.csv", "r") as f1,     open(working_path + r"\PVCombi.csv", "r") as f2,     open(working_path + r"\NMCombi.csv", "r") as f3:

    d1 = range(0,220)
    d2 = range(220,440)
    d3 = range(440,660)
    d4 = range(660,880)
    d5 = range(880,1100)
    d6 = range(1100,1320)
    d7 = range(1320,1540)
    d8 = range(1540,1760)
    d9 =range(1760,1980)
    
    for line_id, (line1, line2, line3) in enumerate(zip(f1, f2, f3)):
        bus_combi = line1.strip("\n").split(",")
        pv_combi = line2.strip("\n").split(",")
        nm_combi = line3.strip("\n").split(",")

        x = 0
        if line_id in d1: x = 1
        elif line_id in d2: x = 2
        elif line_id in d3: x = 3
        elif line_id in d4: x = 4
        elif line_id in d5: x = 5
        elif line_id in d6: x = 6
        elif line_id in d7: x = 7
        elif line_id in d8: x = 8
        elif line_id in d9: x = 9
      

        # Reset DSS
        dssObj.ClearAll()
        
        # Compile DSS file
        dssText.Command = "compile '{0}'".format(working_path + r'.\time_series_python.dss')

        # Add PV and NM load shapes
        dssText.Command = r"Redirect '.\PV_LoadShapes.txt'"
        dssText.Command = r"Redirect '.\NM_LoadShapes.txt'"

        # Add load definitions
        dssText.Command = r"Redirect '.\Loads\Loads_{0}.txt'".format(line_id+1)

        # Add PV definitions
        if line2 != "n/a\n":
            dssText.Command = r"Redirect '.\PV\PV_{0}.txt'".format(line_id+1)

        # Add meter monitors
        dssText.Command = r"Redirect '.\Monitor C1.txt'"

        # Extra stuff
        dssText.Command = r"Set voltagebases=[11  .416]"
        dssText.Command = r"Calcvoltagebases"

        dssText.Command = r"buscoords '.\Buscoords.txt'"
        dssSolution.Solve()

        dssText.Command = r"Set mode=yearly number=336 stepsize=30m"
        #dssText.Command = r"Set Year=1"

        # Solve the circuit
        dssSolution.Solve()

        # Export monitor data
        dssText.Command = r"Redirect '.\Export Monitor C1.txt'"

        # Close demand interval files
        dssText.Command = "closedi"

        # Move simulation results to own folder
        files = os.listdir(working_path)
        path = r"\Simulations\Dataset_{1}\sim_{0}".format(line_id+1, x)
        dest = working_path + path
        os.makedirs(dest, exist_ok=True)
        for f in files:
            if f.startswith("LV_Feeder"):
                shutil.move(os.path.join(working_path, f), os.path.join(dest, f))

        with open(dest + "\info.txt", "w") as f:
            print("Loads:", file=f)
            print(*bus_combi, sep=",", file=f)
            print("PV Generators:", file=f)
            print(*pv_combi, sep=",", file=f)
            print("Net metering:", file=f)
            print(*nm_combi, sep=",", file=f)
        
        if line2 != "n/a\n":
            print("Simulation with PV/NM {0}.. Finished!".format(line_id+1))
        else:
            print("Simulation {0}.. Finished!".format(line_id+1))
            
    print("Done.")


# In[ ]:




