
"""
Merges the daily readings into a single dataset with the benign and malicious data labeled as 0 and 1 respectively. 
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
from pandas import *
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
            if(file.endswith(".csv") and "day_" in file):
                files_actual.append(os.path.join(root,file))
    
    return files_actual


# Create subfolder for merged datasets
Path(r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM5\Merged_Datasets").mkdir(parents=True, exist_ok=True)

filepath = r"C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM5"

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

# Create column names
fields = ['cm_1_power', 'cm_2_power', 
            'load_1_power','load_2_power','load_3_power','load_4_power','load_5_power','load_6_power','load_7_power','load_8_power','load_9_power','load_10_power','load_11_power',
            'load_12_power','load_13_power','load_14_power','load_15_power','load_16_power','load_17_power','load_18_power','load_19_power','load_20_power','load_21_power','load_22_power',
            'load_23_power','load_24_power','load_25_power','load_26_power','load_27_power','load_28_power','load_29_power','load_30_power','load_31_power','load_32_power','load_33_power',
            'load_34_power','load_35_power','load_36_power','load_37_power','load_38_power','load_39_power','load_40_power','load_41_power','load_42_power','load_43_power','load_44_power',
            'load_45_power','load_46_power','load_47_power','load_48_power','load_49_power','load_50_power','load_51_power','load_52_power','load_53_power','load_54_power','load_55_power',
            'label', 'id']

# Iterate through each sim subfolder.
rows = []
count = 0
for sim in sim_subfolders:
    print("Currently in {0}".format(sim))
    
    # Iterate through .csv files summed per day in the current sim folder.
    queue = get_jobs(sim)
    queue.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    for file in queue: 
        filename = file.split('\\')[-1]
        subfolder = file.split('\\')[-2]
        dataset = file.split('\\')[-3]
        
        print("Currently in {0}".format(file))
        
        count += 1
              
        df = pd.read_csv(file).astype(float)
        rows.append(df)
        
        
        if count == 3080:
            temp_df = pd.concat(rows, axis = 1)
            trans_df = temp_df.T
            trans_df.columns = fields
            trans_df.to_csv(r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Simulations - CM5\Merged_Datasets\{}.csv'.format(dataset), index=None)
            rows = []
            count = 0



