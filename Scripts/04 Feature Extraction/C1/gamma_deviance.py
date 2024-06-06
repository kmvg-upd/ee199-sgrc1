#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

def df_gamma_deviance(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    # Chage depending on CM Configuration
    cm_members = [[1, 3],[2, 6],[4, 5],[7, 8,12],[9, 10,11],[14, 13,16],[15, 17],[21, 19],[20, 22],[18, 23],[34, 30,25],[31, 29],[37, 36],[33, 35],[24, 28,27],[26, 44],[32, 38],[46, 48,49],[42, 39, 40],[54, 51],[41, 45],[43, 47],[52, 55],[50, 53]]
    df_gamma = df
    
    # Relative error formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df_gamma['gamma_{}'.format(index)] = 2*(np.log10(abs(sum/df['cm_{}_power'.format(index)]))+abs((df['cm_{}_power'.format(index)]/sum))-1)
    
    # Remove cm columns.
    df_gamma = df_gamma.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    # Chage depending on CM Configuration
    df_gamma = df[['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6', 'gamma_7', 'gamma_8', 'gamma_9', 'gamma_10', 'gamma_11', 'gamma_12', 'gamma_13', 'gamma_14', 'gamma_15', 'gamma_16', 'gamma_17', 'gamma_18', 'gamma_19', 'gamma_20', 'gamma_21', 'gamma_22', 'gamma_23', 'gamma_24'] + [c for c in df if c not in ['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5', 'gamma_6', 'gamma_7', 'gamma_8', 'gamma_9', 'gamma_10', 'gamma_11', 'gamma_12', 'gamma_13', 'gamma_14', 'gamma_15', 'gamma_16', 'gamma_17', 'gamma_18', 'gamma_19', 'gamma_20', 'gamma_21', 'gamma_22', 'gamma_23', 'gamma_24']]]
    df_gamma = df_gamma.drop(df.filter(regex='cm').columns, axis=1)
    df_gamma = df_gamma.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv. Changefilename
    df_gamma.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Gamma_Deviance' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[2]:

#Changefilename
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_1.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_2.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_3.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_4.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_5.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_6.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_7.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_8.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C1\Dataset_9.csv')



# In[ ]:




