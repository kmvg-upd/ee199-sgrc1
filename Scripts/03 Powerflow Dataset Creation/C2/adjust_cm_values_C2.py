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

filepath = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM2"

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
    cm_1ph = [[] for i in range(10)]
    
    
    for file in queue:
        filename = file.split('\\')[-1]
        
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                line_values = line.split(',')
                if i > 0:
                    if "_cm1_" in filename:
                        cm_1ph[0].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm2_" in filename:
                        cm_1ph[1].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm3_" in filename:
                        cm_1ph[2].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm4_" in filename:
                        cm_1ph[3].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm5_" in filename:
                        cm_1ph[4].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm6_" in filename:
                        cm_1ph[5].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm7_" in filename:
                        cm_1ph[6].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm8_" in filename:
                        cm_1ph[7].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm9_" in filename:
                        cm_1ph[8].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm10_" in filename:
                        cm_1ph[9].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    

                    else: print("ERROR")

    cm_1ph = np.array(cm_1ph)
    
    # Adjust cm values based on designated area
    
    cm_adj = cm_1ph
    
    # cm1' = cm1 - cm2 - cm3 - cm4
    cm_adj[0] = cm_1ph[0] - cm_1ph[1] - cm_1ph[2] - cm_1ph[3]
    
    # cm2' = cm2
    cm_adj[1] = cm_1ph[1]
    
    # cm3' = cm3
    cm_adj[2] = cm_1ph[2]
    
    # cm4' = cm4 - cm5 - cm7
    cm_adj[3] = cm_1ph[3] - cm_1ph[4] - cm_1ph[6]
    
    # cm5' = cm5 - cm6
    cm_adj[4] = cm_1ph[4] - cm_1ph[5]
    
    # cm6' = cm6
    cm_adj[5] = cm_1ph[5]
    
    # cm7' = cm7 - cm8 
    cm_adj[6] = cm_1ph[6] - cm_1ph[7] 
    
    # cm8' = cm8 - cm9
    cm_adj[7] = cm_1ph[7] - cm_1ph[8]
    
    # cm9' = cm9 - cm10
    cm_adj[8] = cm_1ph[8] - cm_1ph[9]
    
    # cm10' = cm10 
    cm_adj[9] = cm_1ph[9] 
    
   
    
    cm_adj = np.array(cm_adj)
    
    # Sum per day
    cm_readings = [[] for i in range(10)]
    for i in range(10):
        cm_readings[i].append(sum(cm_adj[i][0:48]))
        cm_readings[i].append(sum(cm_adj[i][48:96]))
        cm_readings[i].append(sum(cm_adj[i][96:144]))
        cm_readings[i].append(sum(cm_adj[i][144:192]))
        cm_readings[i].append(sum(cm_adj[i][192:240]))
        cm_readings[i].append(sum(cm_adj[i][240:288]))
        cm_readings[i].append(sum(cm_adj[i][288:336]))
    
    
    for i in range(10):
        filename = f'\cm_adj_{i+1}.csv'
        np.savetxt(sim + filename, cm_readings[i], delimiter = "\n", fmt="%.6f")