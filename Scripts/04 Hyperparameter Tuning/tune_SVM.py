
"""
Tunes the hyperparameters per dataset, and outputs in a csv file. 
"""

# Import libraries.
import numpy as np
import pandas as pd
import sklearn

from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

# Split data for training and testing 
def id_train(data):
    df = data
    index = []
    for i in range(2464):
        if i%4 == 1 or i%4 == 2:
            index.append(i)
        i+=1
            
    df = df.drop(df.index[index])
    return df

def id_test(data):
    df = data
    index = []
    for i in range(616):
        if i%4 == 1 or i%4 == 2:
            index.append(i)
        i+=1
            
    df = df.drop(df.index[index])
    return df

# Perform SVM
def run_svm(filepath):
    
    # Read csv.
    df = pd.read_csv(filepath)
    df['id'] = np.divmod(np.arange(len(df)),2)[0]+1
    
    train_inds, test_inds = next(GroupShuffleSplit(test_size=0.20, n_splits=2).split(df, groups=df['id']))
    x_train = df.iloc[train_inds].drop(columns=['label', 'id'])
    x_test = df.iloc[test_inds].drop(columns=['label','id'])
    y_train = df.iloc[train_inds]['label'].astype(float)
    y_test = df.iloc[test_inds]['label'].astype(float)
    
    x_train = id_train(x_train)
    x_test = id_test(x_test)
    y_train = id_train(y_train)
    y_test = id_test(y_test)
    
    sc = StandardScaler()
    x_train_scaled = sc.fit_transform(x_train)
    x_test_scaled = sc.transform(x_test)

    param_grid = [{'C': [0.1, 1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001]}]    
    grid_search = GridSearchCV(SVC(), param_grid, scoring = 'accuracy', cv = 10, n_jobs = 1, verbose = 3)

    # Fit the scaled training data to grid-search
    grid_search = grid_search.fit(x_train_scaled, y_train)
    accuracy = grid_search.best_score_
    
    y_pred = grid_search.predict(x_test_scaled) 
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    acc = (tp + tn) / (tn + fp + fn + tp)

    return grid_search.best_params_

# Arrays to store accuracy results
c_gd = []
c_lcl = []
c_ple =[]
c_pd =[]

y_gd = []
y_lcl = []
y_ple =[]
y_pd =[]

# Run SVM 
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Gamma_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_svm(filename)
        c_gd.append(hyperparam["C"])
        y_gd.append(hyperparam["gamma"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Log_Cosh_loss'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_svm(filename)
        c_lcl.append(hyperparam["C"])
        y_lcl.append(hyperparam["gamma"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Percent_Loss_Error'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_svm(filename)
        c_ple.append(hyperparam["C"])
        y_ple.append(hyperparam["gamma"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Poisson_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_svm(filename)
        c_pd.append(hyperparam["C"])
        y_pd.append(hyperparam["gamma"])

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
                    'C': c_gd,
                    'Gamma': y_gd})

df2 = pd.DataFrame({'Feature': ["Log Cosh Loss" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'C': c_lcl,
                    'Gamma': y_lcl})

df3 = pd.DataFrame({'Feature': ["Percent Loss Error" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'C': c_ple,
                    'Gamma': y_ple})

df4 = pd.DataFrame({'Feature': ["Poisson Deviance" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'C': c_pd,
                    'Gamma': y_pd})


data = pd.concat([df, df2], ignore_index=True)
data = pd.concat([data, df3], ignore_index=True)
data = pd.concat([data, df4], ignore_index=True)

# Create CSV
data.to_csv(r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Algorithms - no optimization\SVM_trial.csv', index=None)




