"""
Creates several copies of the benign and malicious dataset from C1, and saves it under C2 to C6. 
"""

import os
from pathlib import Path
import numpy as np
import re
import cmath
import math
import shutil

def get_jobs(filepath):
    '''
    Returns a list of log file paths (STR) to be processed next.
    '''
    files_actual = []

    for root, dirs, files in os.walk(filepath):
        for file in files:
            #append the file name to the list
            if(file.endswith(".csv") and ("hm_ben" in file or "hm_mal_" in file)):
                files_actual.append(os.path.join(root,file))
    
    return files_actual

#### Edit path
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
    
    # Iterate through each .csv in the current sim folder
    queue = get_jobs(sim)
    
    # Iterate through each file
    for file in queue:
        filename = file.split('\\')[-1]
        subfolder = file.split('\\')[-2]
        dataset = file.split('\\')[-3]
        
        #### Edit path
        #duplicate files
        dest_cm2 = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM2" + r'\{}'.format(dataset) + r'\{}'.format(subfolder) + r'\{}'.format(filename)
        dest_cm3 = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM3" + r'\{}'.format(dataset) + r'\{}'.format(subfolder) + r'\{}'.format(filename)
        dest_cm4 = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM4" + r'\{}'.format(dataset) + r'\{}'.format(subfolder) + r'\{}'.format(filename)
        dest_cm5 = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM5" + r'\{}'.format(dataset) + r'\{}'.format(subfolder) + r'\{}'.format(filename)
        dest_cm6 = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM6" + r'\{}'.format(dataset) + r'\{}'.format(subfolder) + r'\{}'.format(filename)
        shutil.copy(file, dest_cm2)
        shutil.copy(file, dest_cm3)
        shutil.copy(file, dest_cm4)
        shutil.copy(file, dest_cm5)
        shutil.copy(file, dest_cm6)
        
        