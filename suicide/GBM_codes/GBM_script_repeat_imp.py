import pandas as pd 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import time

from dataloader_imp import load_data, sui_index, remove_nan, fill_nan, under_sampling
from model_type import select_model, define_args

import argparse
def get_args():
    parser = argparse.ArgumentParser(description='Suicide Prediction Using Gradient Boosting Classifier', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', type=str, help='Model type', dest='model')
    parser.add_argument('-d', '--data', type=str, choices=['idP', 'idA', 'att', 'ideation', 'all'], help='Suicide data type', dest='data')
    parser.add_argument('-dn', '--drop_na', type=bool, default=True, help='Drop NAs', dest='drop_na')
    parser.add_argument('-i', '--interaction', type=bool, default=False, help='Add interaction term', dest='interact')
    return parser.parse_args()

##### Select Model
args_ = get_args()
model = 'Model'+args_.model
data = args_.data
drop_na = args_.drop_na
interact = args_.interact
print(f'Selected Model: {model}, {data}')
print(f'Add Interaction Term? {interact}')
print(f'Dropping NAs? {drop_na}\n')
args = select_model(model, data)

##### Load Data
X_train, y_train, X_test, y_test = load_data(args)

##### Handling NA values
if drop_na:
    print('Dropping nan values...')
    print('Train set: ')
    X_train_, y_train_ = remove_nan(X_train, y_train)
    print('Test set: ')
    X_test_, y_test_ = remove_nan(X_test, y_test)
else:
    print('Filling nan values to mean...\n')
    X_train_, y_train_ = fill_nan(X_train, y_train)
    X_test_, y_test_ = fill_nan(X_test, y_test)

k_fold = 4
N_ESTIMATORS = []
MAX_DEPTH = []
AUC = []
TN = []
FP = []
FN = []
TP = []
ACC = []
for i in range(5):
    print(f'[{i}]-----')
    ##### Under sampling
    X_train, y_train = under_sampling(X_train_, y_train_)
    X_test, y_test = under_sampling(X_test_, y_test_)
    print(f'Check #: {len(X_test)} {len(y_test)} {len(X_train)} {len(y_train)}\n')

    ##### Make it into numpy array
    X_train = X_train.to_numpy()
    y_train = y_train.to_numpy().ravel()
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy().ravel()

    ##### Model design
    cv = StratifiedKFold(n_splits = k_fold, shuffle=True, random_state = 123)
    params = {'n_estimators': np.arange(150, 200, 10),
                'max_depth': np.arange(5, 20, 3)}
    gbc = GradientBoostingClassifier()
    gbc_grid = GridSearchCV(estimator = gbc, param_grid = params, cv = cv, scoring='roc_auc', n_jobs=-1, return_train_score=True)

    ##### Fitting the model
    gbc_grid.fit(X_train, y_train)
    print("Fitting Ends: ")
    now = time.localtime()
    print ("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

    ##### Validate the model
    y_pred_test = gbc_grid.predict(X_test)
    y_proba_test = gbc_grid.predict_proba(X_test)
    y_decision_test = gbc_grid.decision_function(X_test)
    y_result = pd.DataFrame(columns=['y_test', 'y_proba', 'y_decision'])
    y_result['y_test'] = y_test
    y_result['y_proba'] = y_proba_test
    y_result['y_decision'] = y_decision_test
    y_result.to_csv(f"result/{model}_{args.type}{i}_y-predict.csv", index=False)

    best_est = gbc_grid.best_estimator_
    pd.DataFrame(best_est.feature_importances_).to_csv(f"result/{model}_{args.type}{i}_feature.csv", index = False)

    N_ESTIMATORS.append(gbc_grid.best_params_['n_estimators'])
    MAX_DEPTH.append(gbc_grid.best_params_['max_depth'])
    AUC.append(gbc_grid.best_score_)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred_test).ravel()
    TN.append(tn)
    FP.append(fp)
    FN.append(fn)
    TP.append(tp)

    ACC.append(accuracy_score(y_test, y_pred_test))

    print('\n')
    print('best train parameter: ', gbc_grid.best_params_)
    print('best score: ', gbc_grid.best_score_)
    print('\n')


print('------Test Result------')
print('NE MD AUC  SEN SPE PPV NPV ACC')
print(sum(N_ESTIMATORS)/len(N_ESTIMATORS))
print(sum(MAX_DEPTH)/len(MAX_DEPTH))
print(sum(AUC)/len(AUC))
tn_ = sum(TN)/len(TN)
fp_ = sum(FP)/len(FP)
fn_ = sum(FN)/len(FN)
tp_ = sum(TP)/len(TP)
print(tp_/(tp_+fn_))
print(tn_/(tn_+fp_))
print(tp_/(tp_+fp_))
print(tn_/(tn_+fn_))
print(sum(ACC)/len(ACC))
print(f'TN:{tn_}, FP:{fp_}, FN:{fn_}, TP:{tp_}')

print(f'Selected Model: {model}, {data}')
print(f'Dropping NAs? {drop_na}\n')

print('\n')