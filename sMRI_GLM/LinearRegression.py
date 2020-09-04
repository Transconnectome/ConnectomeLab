# Linear Regression + Pearson correlation
# part1 and part2 are converged

import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import Imputer
from scipy import stats

# Import files
print('=====Start Importing Files=====')
data1 = pd.read_csv('/home/ubuntu/SEOYOON/BRAIN_structural/Data/abcd_smrip101_merged_with_GPS.csv', header=0)
data2 = pd.read_csv('/home/ubuntu/SEOYOON/BRAIN_structural/Data/abcd_smrip201_merged_with_GPS.csv', header=0)

# get only sMRI data
imp1 = Imputer(missing_values = np.nan, strategy = 'mean')
X1 = data1.iloc[:, 37:-2]
X1 = imp1.fit_transform(X1.values)
imp2 = Imputer(missing_values = np.nan, strategy = 'mean')
X2 = data2.iloc[:, 35:-3]
X2 = imp2.fit_transform(X2.values)

# Do linear regression for each GPS
print('=====Start Linear Regression=====')
count = 1
for target in data1.iloc[:,1:27].columns:
    print('[{}] {}'.format(count, target))
    y = data1[target]
    y.values.ravel()
    result = []
    
    # part 1
    for col in range(749):
        x = X1[:,col]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        pearsonr, p = stats.pearsonr(x, y)
        result.append([col+37, data1.columns[col+37], slope, intercept, r_value, p_value, std_err, pearsonr, p])
    # part 2
    for col in range(437):
        x = X2[:,col]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        pearsonr, p = stats.pearsonr(x, y)
        result.append([col+35, data2.columns[col+35], slope, intercept, r_value, p_value, std_err, pearsonr, p])

    print('=====Linear Regression is Successively  Done=====')
    scipy_result = pd.DataFrame(result, columns=['col_num', 'label', 'slope', 'intercept', 'r_value', 'p_value', 'std_err', 'pearson_r', 'pearson_p'])
    scipy_result.to_csv('_LR_result/sMRI_'+target+'_LinearRegression_Pearson.csv', index=False)
    print('======The csv File is Generated=====')
