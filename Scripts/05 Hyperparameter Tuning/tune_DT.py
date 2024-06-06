"""
Tunes the hyperparameters per dataset, and outputs in a csv file. 
"""

# Import libraries.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
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

# Perform DT
def run_dt(filepath):
    
    # Read csv.
    df = pd.read_csv(filepath)
    df['id'] = np.divmod(np.arange(len(df)),2)[0]+1
    
    train_inds, test_inds = next(GroupShuffleSplit(test_size=0.20, n_splits=2).split(df, groups=df['id']))
    x_train = df.iloc[train_inds].drop(columns=['label', 'id'])
    x_test = df.iloc[test_inds].drop(columns=['label', 'id'])
    y_train = df.iloc[train_inds]['label'].astype(float)
    y_test = df.iloc[test_inds]['label'].astype(float)
    
    # Train test split
    x_train = id_train(x_train)
    x_test = id_test(x_test)
    y_train = id_train(y_train)
    y_test = id_test(y_test)
    
    # Feature scale.
    sc = StandardScaler()
    x_train_scaled = sc.fit_transform(x_train)
    x_test_scaled = sc.transform(x_test)
    
    
    param_grid = {
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
    }
    
    dtree_reg = DecisionTreeClassifier(random_state=0) # Initialize a decision tree regressor
    grid_search = GridSearchCV(estimator=dtree_reg, param_grid=param_grid, 
                               cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
    
    # Fit the scaled training data to grid-search
    grid_search = grid_search.fit(x_train_scaled, y_train)
    accuracy = grid_search.best_score_
    
    return grid_search.best_params_


# Arrays to store accuracy results
s_gd = []
s_lcl = []
s_ple =[]
s_pd =[]

l_gd = []
l_lcl = []
l_ple =[]
l_pd =[]

# Run DT 
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Gamma_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_dt(filename)
        s_gd.append(hyperparam["min_samples_split"])
        l_gd.append(hyperparam["min_samples_leaf"])
        
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Log_Cosh_loss'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_dt(filename)
        s_lcl.append(hyperparam["min_samples_split"])
        l_lcl.append(hyperparam["min_samples_leaf"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Percent_Loss_Error'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_dt(filename)
        s_ple.append(hyperparam["min_samples_split"])
        l_ple.append(hyperparam["min_samples_leaf"])
        
for cm in range(6):
    for dataset in range(5):
        filename = r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199' + r'\C{} Features'.format(cm+1) + '\Poisson_Deviance'+ r'\Dataset_{}.csv'.format(dataset+1)
        print("Currently in {0}".format(filename))
        hyperparam = run_dt(filename)
        s_pd.append(hyperparam["min_samples_split"])
        l_pd.append(hyperparam["min_samples_leaf"])

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
                    'Min Split': s_gd,
                    'Min Leaf': l_gd})

df2 = pd.DataFrame({'Feature': ["Log Cosh Loss" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Min Split': s_lcl,
                    'Min Leaf': l_lcl})

df3 = pd.DataFrame({'Feature': ["Percent Loss Error" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Min Split': s_ple,
                    'Min Leaf': l_ple})

df4 = pd.DataFrame({'Feature': ["Poisson Deviance" for i in range(5*6)],
                    'Check Meter Config': cm_labels,
                    'Dataset': dataset_labels,
                    'Min Split': s_pd,
                    'Min Leaf': l_pd})

data = pd.concat([df, df2], ignore_index=True)
data = pd.concat([data, df3], ignore_index=True)
data = pd.concat([data, df4], ignore_index=True)

# Create CSV
data.to_csv(r'C:\Users\kaira\Documents\00_UP\04 Fourth Year\Second Sem\EE 199\Algorithms - no optimization\DT_trial.csv', index=None)
