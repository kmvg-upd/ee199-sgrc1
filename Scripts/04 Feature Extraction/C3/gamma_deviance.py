#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

def df_gamma_deviance(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    # Chage depending on CM Configuration
    cm_members = [[1,2,3,4,5,6,7,8,9,10,11,12],[13,14,15,16,17,18,19,20,21,22,23],[34,30,25,31,29,37,36,33,35],[24,28,27,26,44,32,38,46,48,49,42,39],[40,54,51,41,45,43,47,52,55,50,53]]
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
    df_gamma = df[['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5'] + [c for c in df if c not in ['gamma_1', 'gamma_2', 'gamma_3', 'gamma_4', 'gamma_5']]]
    df_gamma = df_gamma.drop(df.filter(regex='cm').columns, axis=1)
    df_gamma = df_gamma.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv. Changefilename
    df_gamma.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Gamma_Deviance' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[2]:

#Changefilename
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_1.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_2.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_3.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_4.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_5.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_6.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_7.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_8.csv')
df_gamma_deviance(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C3\Dataset_9.csv')


# In[ ]:




