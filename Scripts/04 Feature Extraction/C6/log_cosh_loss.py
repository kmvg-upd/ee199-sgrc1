#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

def df_log_cosh(filepath):
    
    # Initialize csv and 55 houses.
    df = pd.read_csv(filepath)
    cm_members = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55]]
    df_log = df
    
    # Log cosh loss formula.
    for index, cm in enumerate(cm_members, 1):
        sum = 0
        for load in cm:
            sum = sum + df['load_{}_power'.format(load)]
        df_log['log_cosh_{}'.format(index)] = np.log10(np.cosh(abs(sum -  df['cm_{}_power'.format(index)])))
    
    # Remove cm columns.
    df_log = df_log.astype({col: 'float32' for col in df.select_dtypes('int64').columns})
    df_log = df[['log_cosh_1'] + [c for c in df if c not in ['log_cosh_1']]]
    df_log = df_log.drop(df.filter(regex='cm').columns, axis=1)
    df_log = df_log.drop(df.filter(regex='load').columns, axis=1)
    
    # Save as csv.
    df_log.to_csv(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Log_Cosh_Loss' + r'\{}'.format(filepath.split('\\')[-1]), index = False)
    print("Finished {}".format(filepath.split('\\')[-1]))


# In[2]:


df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_1.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_2.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_3.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_4.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_5.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_6.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_7.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_8.csv')
df_log_cosh(r'C:\Users\ferre\OneDrive\Documents\Thesis Files\Feature Extraction\C4\Dataset_9.csv')




# In[ ]:




