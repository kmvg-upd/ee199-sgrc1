
"""
Consolidates the household and check meter readings for a certain day in a new csv file. 
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
            if(file.endswith(".csv") and ("cm_adj" in file or "hm_ben" in file or "hm_mal_" in file)):
                files_actual.append(os.path.join(root,file))
    
    return files_actual


filepath = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM4"

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
    
    # Create arrays for each day
    d_ben = [[[] for i in range(4+55+3)] for i in range(7)]
    d_mal = [[[] for i in range(4+55+3)] for i in range(7)]
    
    
    # Iterate through each .csv in the current sim folder
    queue = get_jobs(sim)
    
    # Iterate through each file
    for file in queue:
        filename = file.split('\\')[-1]
        subfolder = file.split('\\')[-2]
        dataset = file.split('\\')[-3]
        simnum = [int(s) for s in re.findall(r'\d+', subfolder)]
        filenum = [int(s) for s in re.findall(r'\d+', filename)]
        fileindex = filenum[0]
        
        # CM files
        if "cm_adj" in filename: 
            with open(file, 'r') as f:
                for i, line in enumerate(f):
                    line_values = line.split(',')
                    d_ben[i][fileindex].append(float(line_values[0]))
                    d_mal[i][fileindex].append(float(line_values[0]))
                    
        # HM_Ben files
        elif "hm_ben" in filename:       
            with open(file, 'r') as f:
                for i, line in enumerate(f):
                    line_values = line.split(',')
                    d_ben[i][4+fileindex].append(float(line_values[0]))
                    
        # HM_Mal files
        elif "hm_mal_" in filename:       
            with open(file, 'r') as f:
                for i, line in enumerate(f):
                    line_values = line.split(',')
                    d_mal[i][4+fileindex].append(float(line_values[0]))
    
   
    for i in range(7):
        
        # Label 0 if benign, 1 if malicious
        d_ben[i][0].append(0)
        d_mal[i][0].append(0)
        
        
        # Label 0 if benign, 1 if malicious
        d_ben[i][4+55+1].append(0)
        d_mal[i][4+55+1].append(1)
   
        # Label id
        if simnum[0]%220 == 0:
            newsim = 220-1
        else: 
            newsim = (simnum[0]%220-1)
            
        d_ben[i][4+55+2].append(newsim*7 + (i+1))
        d_mal[i][4+55+2].append(newsim*7 + (i+1))
        
        

    # Create files 
    for i in range(7):
        filename = f'\day_ben_{i+1}.csv'
        np.savetxt(sim + filename, d_ben[i], delimiter = "\n", fmt="%.6f")
        
    for i in range(7):
        filename = f'\day_mal_{i+1}.csv'
        np.savetxt(sim + filename, d_mal[i], delimiter = "\n", fmt="%.6f")