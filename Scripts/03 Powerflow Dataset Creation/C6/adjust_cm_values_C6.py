"""
Adjusts the check meter readings to only measure power flow in their assigned area, and sums the meter readings per day 
"""

import os
from pathlib import Path
import numpy as np
import re
import cmath
import math

def get_jobs(filepath):
    '''
    Returns a list of log file paths (STR) to be processed next.
    '''
    files_actual = []

    for root, dirs, files in os.walk(filepath):
        for file in files:
            #append the file name to the list
            if(file.endswith(".csv") and "_cm" in file):
                files_actual.append(os.path.join(root,file))
    
    return files_actual

filepath = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM6"

sim_subfolders = []

# Get list of sim_X folders
for dataset_folder in os.scandir(filepath):
    if dataset_folder.is_dir():
        print("Found dataset folder: {0}".format(dataset_folder.path))
        for f in os.scandir(dataset_folder.path):
            sim_word = f.path.split("\\")[-1].split("_")[0]
            if f.is_dir() and 'sim' in sim_word:
                sim_subfolders.append(f.path)

sim_subfolders.sort(key=lambda f: int(re.sub('\D', '', f)))

# Iterate through each sim subfolder
for sim in sim_subfolders:
    print("Currently in {0}".format(sim))
    
    # Iterate through each cm .csv in the current sim folder
    queue = get_jobs(sim)
    cm_1ph = []
    
    
    for file in queue:
        filename = file.split('\\')[-1]
        
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                line_values = line.split(',')
                if i > 0:
                    if "_cm1_" in filename:
                        cm_1ph.append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    

                    else: print("ERROR")

    cm_1ph = np.array(cm_1ph)
    
    # Sum per day
    cm_readings = []

    cm_readings.append(sum(cm_1ph[0:48]))
    cm_readings.append(sum(cm_1ph[48:96]))
    cm_readings.append(sum(cm_1ph[96:144]))
    cm_readings.append(sum(cm_1ph[144:192]))
    cm_readings.append(sum(cm_1ph[192:240]))
    cm_readings.append(sum(cm_1ph[240:288]))
    cm_readings.append(sum(cm_1ph[288:336]))
    
    
    
    filename = '\cm_adj_1.csv'
    np.savetxt(sim + filename, cm_readings, delimiter = "\n", fmt="%.6f")
    