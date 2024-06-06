#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import math

def df_poisson_deviance(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    cm_members = [[1, 3],[2, 6],[4, 5],[7, 8,12],[9, 10,11],[14, 13,16],[15, 17],[21, 19],[20, 22],[18, 23],[34, 30,25],[31, 29],[37, 36],[33, 35],[24, 28,27],[26, 44],[32, 38],[46, 48,49],[42, 39, 40],[54, 51],[41, 45],[43, 47],[52, 55],[50, 53]]
    df_poisson = df
    
    # Gamma deviance formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df_poisson['poisson_{}'.format(index)] = 2*(df['cm_{}_power'.format(index)]*np.log10(abs(df['cm_{}_power'.format(index)]/sum))+sum-df['cm_{}_power'.format(index)])
    
    # Remove cm columns.
    df_poisson = df_poisson.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    df_poisson = df[['poisson_1', 'poisson_2', 'poisson_3', 'poisson_4', 'poisson_5', 'poisson_6', 'poisson_7', 'poisson_8', 'poisson_9', 'poisson_10', 'poisson_11', 'poisson_12', 'poisson_13', 'poisson_14', 'poisson_15', 'poisson_16', 'poisson_17', 'poisson_18', 'poisson_19', 'poisson_20', 'poisson_21', 'poisson_22', 'poisson_23', 'poisson_24'] + [c for c in df if c not in ['poisson_1', 'poisson_2', 'poisson_3', 'poisson_4', 'poisson_5', 'poisson_6', 'poisson_7', 'poisson_8', 'poisson_9', 'poisson_10', 'poisson_11', 'poisson_12', 'poisson_13', 'poisson_14', 'poisson_15', 'poisson_16', 'poisson_17', 'poisson_18', 'poisson_19', 'poisson_20', 'poisson_21', 'poisson_22', 'poisson_23', 'poisson_24']]]
    df_poisson = df_poisson.drop(df.filter(regex='cm').columns, axis=1)
    df_poisson = df_poisson.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv.
    df_poisson.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Poisson_Deviance' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[4]:


df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_1.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_2.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_3.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_4.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_5.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_6.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_7.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_8.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_9.csv')



# In[ ]:




