
"""
Tunes the hyperparameters per dataset, and outputs in a csv file. 
"""

import pandas as pd
import numpy as np
from time import time
from scipy.stats import randint, loguniform
from sklearn.neural_network import MLPClassifier
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import RandomizedSearchCV, RepeatedStratifiedKFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


def run_ann(filepath,c):

    df = pd.read_csv(filepath)
    
    if c==0:
        col=25 
    elif c==1:
        col=11
    elif c==2:
        col=6
    elif c==3:
        col=5 
    elif c==4:
        col=3
    elif c==5:
        col=2
    
    df.drop(df.columns[col], axis=1, inplace=True)
    X, y = df.iloc[:,:-1].to_numpy(), df.iloc[:,-1].to_numpy()

    
    # Split into 70% training, 30% testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5, stratify=y)
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    
    model_params = {'solver': ['adam'],
                    'activation': ['relu'],
                    'batch_size': [32, 64],
                    'learning_rate': ['constant'],
                    'learning_rate_init': [0.001, 0.01, 0.1]
                    }
    
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3)
    
    n_iter = 50
    grid_search = GridSearchCV(MLPClassifier(max_iter=100), param_grid=model_params, n_jobs=1, cv=5, verbose=3)

    
    grid_search.fit(X_train, y_train)
    
    # Print best parameters after tuning
    return grid_search.best_params_


# Arrays to store accuracy results
s_gd = []
s_lcl = []
s_ple =[]
s_pd =[]

a_gd = []
a_lcl = []
a_ple =[]
a_pd =[]

b_gd = []
b_lcl = []
b_ple =[]
b_pd =[]


# Run SVM 
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Gamma_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_ann(filename,cm)
        s_gd.append(hyperparam["batch_size"])
        a_gd.append(hyperparam["learning_rate_init"])
        # b_gd.append(hyperparam["batch_size"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Log_Cosh_loss'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_ann(filename,cm)
        s_lcl.append(hyperparam["batch_size"])
        a_lcl.append(hyperparam["learning_rate_init"])
        # b_lcl.append(hyperparam["batch_size"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Percent_Loss_Error'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_ann(filename,cm)
        s_ple.append(hyperparam["batch_size"])
        a_ple.append(hyperparam["learning_rate_init"])
        # b_ple.append(hyperparam["batch_size"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Poisson_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_ann(filename,cm)
        s_pd.append(hyperparam["batch_size"])
        a_pd.append(hyperparam["learning_rate_init"])
        # b_pd.append(hyperparam["batch_size"])

# Create data for dataframe columns
cm_labels = []
for cm in range(6):
    for i in range(5):
        cm_labels.append('C{}'.format(cm+1))
        
dataset_labels = []
for i in range(6):
    for j in range(5):
        dataset_labels.append(j+1)
    
# Create dataframe
df = pd.DataFrame({'Feature': ["Gamma Deviance" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Batch Size': s_gd,
                    'LR': a_gd
                    # 'Batch Size': b_gd
                    })

df2 = pd.DataFrame({'Feature': ["Log Cosh Loss" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Batch Size': s_lcl,
                    'LR': a_lcl
                    # 'Batch Size': b_lcl
                    })

df3 = pd.DataFrame({'Feature': ["Percent Loss Error" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Batch Size': s_ple,
                    'LR': a_ple
                    # 'Batch Size': b_gd
                    })

df4 = pd.DataFrame({'Feature': ["Poisson Deviance" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Batch Size': s_pd,
                    'LR': a_pd
                    # 'Batch Size': b_pd
                    })


data = pd.concat([df, df2], ignore_index=True)
data = pd.concat([data, df3], ignore_index=True)
data = pd.concat([data, df4], ignore_index=True)

# Create CSV
data.to_csv(r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Algorithms - no optimization\ANN_trial.csv', index=None)

