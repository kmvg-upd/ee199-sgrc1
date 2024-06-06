#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

def df_error(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    cm_members = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,29,30,31,33,34,35,36,37],[24,26,27,28,32,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55]]
    df_gamma = df
    
    # Relative error formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df['power_error_{}'.format(index)] = abs(df['cm_{}_power'.format(index)] - sum)/abs(df['cm_{}_power'.format(index)])
    
    # Remove cm columns.
    df_gamma = df_gamma.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    df_gamma = df[['power_error_1', 'power_error_2'] + [c for c in df if c not in ['power_error_1', 'power_error_2']]]
    df_gamma = df_gamma.drop(df.filter(regex='cm').columns, axis=1)
    df_gamma = df_gamma.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv.
    df_gamma.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Percent_Loss_Error' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[2]:


df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_1.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_2.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_3.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_4.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_5.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_6.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_7.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_8.csv')
df_error(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C6\Dataset_9.csv')



# In[ ]:




