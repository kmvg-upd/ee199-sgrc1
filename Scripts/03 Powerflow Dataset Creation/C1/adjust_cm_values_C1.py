
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

filepath = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM1"

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
    cm_1ph = [[] for i in range(24)]
    
    
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
                    elif "_cm11_" in filename:
                        cm_1ph[10].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm12_" in filename:
                        cm_1ph[11].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm13_" in filename:
                        cm_1ph[12].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm14_" in filename:
                        cm_1ph[13].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm15_" in filename:
                        cm_1ph[14].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm16_" in filename:
                        cm_1ph[15].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm17_" in filename:
                        cm_1ph[16].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm18_" in filename:
                        cm_1ph[17].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm19_" in filename:
                        cm_1ph[18].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm20_" in filename:
                        cm_1ph[19].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm21_" in filename:
                        cm_1ph[20].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm22_" in filename:
                        cm_1ph[21].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm23_" in filename:
                        cm_1ph[22].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    elif "_cm24_" in filename:
                        cm_1ph[23].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))


                    else: print("ERROR")

    cm_1ph = np.array(cm_1ph)
    
    # Adjust cm values based on designated area
    cm_adj = cm_1ph
    
    # cm1' = cm1 - cm2
    cm_adj[0] = cm_1ph[0] - cm_1ph[1]
    
    # cm2' = cm2 - cm3
    cm_adj[1] = cm_1ph[1] - cm_1ph[2]
    
    # cm3' = cm3 - cm4 - cm6
    cm_adj[2] = cm_1ph[2] - cm_1ph[3] - cm_1ph[5]
    
    # cm4' = cm4 - cm5
    cm_adj[3] = cm_1ph[3] - cm_1ph[4]
    
    # cm5' = cm5 
    cm_adj[4] = cm_1ph[4]
    
    # cm6' = cm6 - cm7 - cm8
    cm_adj[5] = cm_1ph[5] - cm_1ph[6] - cm_1ph[7]
    
    # cm7' = cm7
    cm_adj[6] = cm_1ph[6]
    
    # cm8' = cm8 - cm9 - cm15
    cm_adj[7] = cm_1ph[7] - cm_1ph[8] - cm_1ph[14]
    
    # cm9' = cm9 - cm10
    cm_adj[8] = cm_1ph[8] - cm_1ph[9]
    
    # cm10' = cm10 - cm11 
    cm_adj[9] = cm_1ph[9] - cm_1ph[10] 
    
    # cm11' = cm11 - cm12
    cm_adj[10] = cm_1ph[10]- cm_1ph[11]
    
    # cm12' = cm12 - cm13
    cm_adj[11] = cm_1ph[11] - cm_1ph[12]
    
    # cm13' = cm13 - cm14
    cm_adj[12] = cm_1ph[12] - cm_1ph[13]
    
    # cm14' = cm14 
    cm_adj[13] = cm_1ph[13]
    
    # cm15' = cm15 - cm16
    cm_adj[14] = cm_1ph[14] - cm_1ph[15]
    
    # cm16' = cm16 - cm17 
    cm_adj[15] = cm_1ph[15] - cm_1ph[16]
    
    # cm17' = cm17 - cm18 
    cm_adj[16] = cm_1ph[16] - cm_1ph[17] 
    
    # cm18' = cm18 - cm19
    cm_adj[17] = cm_1ph[17] - cm_1ph[18] 
    
    # cm19' = cm19 - cm20
    cm_adj[18] = cm_1ph[18] - cm_1ph[19]
    
    # cm20' = cm20 - cm21 
    cm_adj[19] = cm_1ph[19] - cm_1ph[20] 
    
    # cm21' = cm21 - cm22
    cm_adj[20] = cm_1ph[20] - cm_1ph[21]
    
    # cm22' = cm22 - cm23
    cm_adj[21] = cm_1ph[21] - cm_1ph[22]
    
    # cm23' = cm23 - cm24
    cm_adj[22] = cm_1ph[22] - cm_1ph[23]
    
    # cm24' = cm24 
    cm_adj[23] = cm_1ph[23]
    
    
    cm_adj = np.array(cm_adj)
    
    
    # Sum per day
    cm_readings = [[] for i in range(24)]
    for i in range(24):
        cm_readings[i].append(sum(cm_adj[i][0:48]))
        cm_readings[i].append(sum(cm_adj[i][48:96]))
        cm_readings[i].append(sum(cm_adj[i][96:144]))
        cm_readings[i].append(sum(cm_adj[i][144:192]))
        cm_readings[i].append(sum(cm_adj[i][192:240]))
        cm_readings[i].append(sum(cm_adj[i][240:288]))
        cm_readings[i].append(sum(cm_adj[i][288:336]))
        
        
    
    
    for i in range(24):
        filename = f'\cm_adj_{i+1}.csv'
        np.savetxt(sim + filename, cm_readings[i], delimiter = "\n", fmt="%.6f")