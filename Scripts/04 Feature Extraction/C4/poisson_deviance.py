#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import math

def df_poisson_deviance(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    cm_members = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,25,29,30,31,33,34,35,36,37],[24,26,27,28,32,38,39,42,44,46,48,49],[40,41,43,45,47,50,51,52,53,54,55]]
    df_poisson = df
    
    # Gamma deviance formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df_poisson['poisson_{}'.format(index)] = 2*(df['cm_{}_power'.format(index)]*np.log10(abs(df['cm_{}_power'.format(index)]/sum))+sum-df['cm_{}_power'.format(index)])
    
    # Remove cm columns.
    df_poisson = df_poisson.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    df_poisson = df[['poisson_1', 'poisson_2', 'poisson_3', 'poisson_4'] + [c for c in df if c not in ['poisson_1', 'poisson_2', 'poisson_3', 'poisson_4']]]
    df_poisson = df_poisson.drop(df.filter(regex='cm').columns, axis=1)
    df_poisson = df_poisson.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv.
    df_poisson.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Poisson_Deviance' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[4]:


df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_1.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_2.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_3.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_4.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_5.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_6.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_7.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_8.csv')
df_poisson_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C5\Dataset_9.csv')


# In[ ]:




