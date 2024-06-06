#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

def df_error(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    cm_members = [[1, 3],[2, 6],[4, 5],[7, 8,12],[9, 10,11],[14, 13,16],[15, 17],[21, 19],[20, 22],[18, 23],[34, 30,25],[31, 29],[37, 36],[33, 35],[24, 28,27],[26, 44],[32, 38],[46, 48,49],[42, 39, 40],[54, 51],[41, 45],[43, 47],[52, 55],[50, 53]]
    df_gamma = df
    
    # Relative error formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df['power_error_{}'.format(index)] = abs(df['cm_{}_power'.format(index)] - sum)/abs(df['cm_{}_power'.format(index)])
    
    # Remove cm columns.
    df_gamma = df_gamma.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    df_gamma = df[['power_error_1', 'power_error_2', 'power_error_3', 'power_error_4', 'power_error_5', 'power_error_6', 'power_error_7', 'power_error_8', 'power_error_9', 'power_error_10', 'power_error_11', 'power_error_12', 'power_error_13', 'power_error_14', 'power_error_15', 'power_error_16', 'power_error_17', 'power_error_18', 'power_error_19', 'power_error_20', 'power_error_21', 'power_error_22', 'power_error_23', 'power_error_24'] + [c for c in df if c not in ['power_error_1', 'power_error_2', 'power_error_3', 'power_error_4', 'power_error_5', 'power_error_6', 'power_error_7', 'power_error_8', 'power_error_9', 'power_error_10', 'power_error_11', 'power_error_12', 'power_error_13', 'power_error_14', 'power_error_15', 'power_error_16', 'power_error_17', 'power_error_18', 'power_error_19', 'power_error_20', 'power_error_21', 'power_error_22', 'power_error_23', 'power_error_24']]]
    df_gamma = df_gamma.drop(df.filter(regex='cm').columns, axis=1)
    df_gamma = df_gamma.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv.
    df_gamma.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Percent_Loss_Error' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[2]:


df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_1.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_2.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_3.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_4.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_5.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_6.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_7.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_8.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_9.csv')


# In[ ]:




