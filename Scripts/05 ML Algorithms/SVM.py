
"""
Extracts the optimal hyperparameters from csv file generated in the hyperparameter tuning stage to train and test the ML classifier.
"""

# Import libraries.
import numpy as np
import pandas as pd
import sklearn

from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix


# Perform SVM
def run_svm(filepath, c, g):
    
    # Read csv.
    df = pd.read_csv(filepath)  
    df.drop(df.columns[-1], axis=1, inplace=True)
    X, y = df.iloc[:,:-1].to_numpy(), df.iloc[:,-1].to_numpy()
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5, stratify=y)
    
    #Scale
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    parameters = [{'C': [c], 'kernel': ['rbf'], 'gamma': [g]}] 
    grid_search = GridSearchCV(estimator = SVC(),
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10,
                           n_jobs = 1, 
                           verbose = 4)

    # Fit the scaled training data to grid-search
    grid_search = grid_search.fit(X_train, y_train)
    accuracy = grid_search.best_score_
    
    y_pred = grid_search.predict(X_test) 
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    acc = (tp + tn) / (tn + fp + fn + tp)
    # pr = tp / (tp + fp)
    # dr = tp / (tp + fn)
    # f1 = (2*dr*pr) / (dr + pr)
    return acc


# Get hyperparameters
filepath = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Algorithms Optimized\SVM_hyperparam.csv'
df = pd.read_csv(filepath) 
C_list = df['C'].tolist()
Gamma_list = df['Gamma'].tolist()

# Arrays to store accuracy results
acc_gd = []
acc_lcl = []
acc_ple =[]
acc_pd =[]

# Run SVM 

# Gamma Deviance
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Gamma_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        C_val = C_list[cm*5 + dataset]
        Gamma_val = Gamma_list[cm*5 + dataset]
        acc_gd.append(run_svm(filename, C_val, Gamma_val))
   
# Log Cosh Loss
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Log_Cosh_loss'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        C_val = C_list[30 + cm*5 + dataset]
        Gamma_val = Gamma_list[30 + cm*5 + dataset]
        acc_lcl.append(run_svm(filename, C_val, Gamma_val))
  
# Percent Loss Error
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Percent_Loss_Error'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        C_val = C_list[60 + cm*5 + dataset]
        Gamma_val = Gamma_list[60 + cm*5 + dataset]
        acc_ple.append(run_svm(filename, C_val, Gamma_val))
 
# Poisson Deviance
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Poisson_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        C_val = C_list[90 + cm*5 + dataset]
        Gamma_val = Gamma_list[90 + cm*5 + dataset]
        acc_pd.append(run_svm(filename, C_val, Gamma_val))

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
                    'Accuracy': acc_gd})

df2 = pd.DataFrame({'Feature': ["Log Cosh Loss" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Accuracy': acc_lcl})

df3 = pd.DataFrame({'Feature': ["Percent Loss Error" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Accuracy': acc_ple})

df4 = pd.DataFrame({'Feature': ["Poisson Deviance" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Accuracy': acc_pd})


data = pd.concat([df, df2], ignore_index=True)
data = pd.concat([data, df3], ignore_index=True)
data = pd.concat([data, df4], ignore_index=True)

# Create CSV
data.to_csv(r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Algorithms Optimized\SVM_results.csv', index=None)



