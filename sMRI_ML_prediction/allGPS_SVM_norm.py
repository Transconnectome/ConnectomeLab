import os
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import KFold, GridSearchCV, train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, Imputer

k_fold = 5

all_data = pd.read_csv('/home/ubuntu/SEOYOON/BRAIN_structural/Data/abcd_smrip101_merged_with_GPS_all.csv', header=0)

scaler = StandardScaler()
imp = Imputer(missing_values = np.nan, strategy = 'mean')
X_raw = all_data.iloc[:, 89:-2].values
X = imp.fit_transform(X_raw)
X = scaler.fit_transform(X)

result = []
gps = all_data.iloc[:, 27:53].columns
for target in gps:
    y = all_data[target]
    y.values.ravel()
    print("\n")
    print("[{}]".format(target))
    outer_cv = KFold(n_splits = k_fold, shuffle=False, random_state = 123)
    loop=1
    for train_index, test_index in outer_cv.split(X, y):
    #     print('='*50)
        print('Loop: ', loop)

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        svr = SVR(C=0.1, gamma=0.01)
        svr.fit(X_train, y_train)
        
        train_sc = svr.score(X_train, y_train)
        test_sc = svr.score(X_test, y_test)
        
        result.append([target, loop, 0.1, 0.01, train_sc, test_sc])
        print("{:.<45}".format("1. 0.01 Train r2 score"))
        print("\t{}".format(train_sc))
        print("{:.<45}".format("2. 0.01 Test r2 score"))
        print("\t{}".format(test_sc))
        
        svr = SVR(C=0.1, gamma='auto')
        svr.fit(X_train, y_train)
        
        train_sc = svr.score(X_train, y_train)
        test_sc = svr.score(X_test, y_test)
        
        result.append([target, loop, 0.1, 'auto', train_sc, test_sc])
        print("{:.<45}".format("1. auto Train r2 score"))
        print("\t{}".format(train_sc))
        print("{:.<45}".format("2. auto Test r2 score"))
        print("\t{}".format(test_sc))
        loop +=1
        
pd.DataFrame(result, columns=['GPS', 'loop', 'C', 'gamma', 'train_score', 'test_score']).to_csv('SVM_prediction_norm.csv', index=False)