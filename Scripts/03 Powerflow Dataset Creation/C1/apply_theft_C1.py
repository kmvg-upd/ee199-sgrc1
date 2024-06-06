
"""
Sums the individual household readings per day, and creates benign and malicious datasets.
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
            if(file.endswith(".csv") and "_hm_load" in file):
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
    
    # Iterate through each hm .csv in the current sim folder
    queue = get_jobs(sim)
    hm_1ph = [[] for i in range(55)]
    
    
    for file in queue:
        filename = file.split('\\')[-1]
        filenum = [int(s) for s in re.findall(r'\d+', filename)]
        fileindex = filenum[0]-1
        
        
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                line_values = line.split(',')
                if i > 0:
                    if "_hm_" in filename:
                        hm_1ph[fileindex].append(float(line_values[2]) + float(line_values[4]) + float(line_values[6]))
                    

                    else: print("ERROR")

    hm_1ph = np.array(hm_1ph)

    # # Create files for 1phase household meter readings
    # for i in range(55):
    #         filename = f'\hm_adj_{i+1}.csv'
    #         np.savetxt(sim + filename, hm_1ph[i], delimiter = "\n", fmt="%.6f")
            
    # Sum readings per day
    hm_ben = [[] for i in range(55)]
    for i in range(55):
        hm_ben[i].append(sum(hm_1ph[i][0:48]))
        hm_ben[i].append(sum(hm_1ph[i][48:96]))
        hm_ben[i].append(sum(hm_1ph[i][96:144]))
        hm_ben[i].append(sum(hm_1ph[i][144:192]))
        hm_ben[i].append(sum(hm_1ph[i][192:240]))
        hm_ben[i].append(sum(hm_1ph[i][240:288]))
        hm_ben[i].append(sum(hm_1ph[i][288:336]))
    
    # Create files for benign dataset
    for i in range(55):
        filename = f'\hm_ben_{i+1}.csv'
        np.savetxt(sim + filename, hm_ben[i], delimiter = "\n", fmt="%.6f")
    
    
    # Apply theft
    simname = sim.split('\\')[-1]
    simnum = [int(s) for s in re.findall(r'\d+', simname)]
    simindex = simnum[0]-1
    
    hm_malraw = hm_1ph
    thief = simindex%55
    ket = np.random.uniform(0.1, 0.8)
    
    for i in range(len(hm_malraw[thief])):

        if hm_malraw[thief][i] >= 0:
            hm_malraw[thief][i] = hm_malraw[thief][i] * ket
            

        else:
            hm_malraw[thief][i] = hm_malraw[thief][i] - (abs(hm_malraw[thief][i]) * ket)
            
    # for i in range(55):
    #     filename = f'\hm_malraw_{i+1}.csv'
    #     np.savetxt(sim + filename, hm_malraw[i], delimiter = "\n", fmt="%.6f")
                
            
    
    # Sum readings per day    
    hm_mal = [[] for i in range(55)]
    for i in range(55):
        hm_mal[i].append(sum(hm_malraw[i][0:48]))
        hm_mal[i].append(sum(hm_malraw[i][48:96]))
        hm_mal[i].append(sum(hm_malraw[i][96:144]))
        hm_mal[i].append(sum(hm_malraw[i][144:192]))
        hm_mal[i].append(sum(hm_malraw[i][192:240]))
        hm_mal[i].append(sum(hm_malraw[i][240:288]))
        hm_mal[i].append(sum(hm_malraw[i][288:336]))
        
    for i in range(55):
        filename = f'\hm_mal_{i+1}.csv'
        np.savetxt(sim + filename, hm_mal[i], delimiter = "\n", fmt="%.6f")
    
    
        
    