import pandas as pd 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import time

from util import get_args
from dataloader import load_data

######### Command Line Arguments #########
args = get_args()
if args.demo and not args.ksad and not args.gps and not args.gps_sig and not args.pheno:
    model = 'Model1'
elif args.demo and args.ksad and not args.gps and not args.gps_sig and not args.pheno:
    model = 'Model2'
elif args.demo and not args.ksad and args.gps and not args.gps_sig and not args.pheno:
    model = 'Model3'
elif args.demo and not args.ksad and not args.gps and args.gps_sig and not args.pheno:
    model = 'Model4'
elif args.demo and not args.ksad and not args.gps and not args.gps_sig and args.pheno:
    model = 'MODEL5'
elif args.demo and not args.ksad and args.gps and not args.gps_sig and args.pheno:
    model = 'Model6'
elif args.demo and not args.ksad and not args.gps and args.gps_sig and args.pheno:
    model = 'Model7'

print(f'Arguments: {args}')
print(f'Model: {model}')

######### Load Data #########
X_train, y_train, X_test, y_test = load_data(args)

######### Model specific constants #########
k_fold = 5

######### Model Design #########
# Cross validation set
cv = StratifiedKFold(n_splits = k_fold, shuffle=True, random_state = 123)
params = {'n_estimators': np.arange(150, 200, 10),
            'max_depth': np.arange(15, 45, 5)}
gbc = GradientBoostingClassifier()
gbc_grid = GridSearchCV(estimator = gbc, param_grid = params, cv = cv, scoring='roc_auc', n_jobs=-1, return_train_score=True)

######### FIT #########
print("Fitting Starts: ")
now = time.localtime()
print ("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
gbc_grid.fit(X_train, y_train)
y_pred_test = gbc_grid.predict(X_test)
print("Fitting Ends: ")
now = time.localtime()
print ("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

######### validate model #########
result = pd.DataFrame(gbc_grid.cv_results_)[['mean_test_score', 'std_test_score', 'params']]
print(result)
result.to_csv(f"result/{model}_{args.type}_score.csv", index=False)
best_est = gbc_grid.best_estimator_
print("Feature Importances:\n{}".format(best_est.feature_importances_))
pd.DataFrame(best_est.feature_importances_).to_csv(f"result/{model}_{args.type}_feature.csv", index = False)
print('\n')
print('best train parameter: ', gbc_grid.best_params_)
print('best train score: ', gbc_grid.best_score_)
print('\n')
print('------Test Result------')
print('test score: ', accuracy_score(y_test, y_pred_test))
print('confusion matrix: ')
print(confusion_matrix(y_test, y_pred_test))
print('\n')
