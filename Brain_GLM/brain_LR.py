# Linear Regression + Pearson correlation
# part1 and part2 are converged

import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import Imputer
from scipy import stats

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Conducting Linear Regression on GPS and Brain', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--mor', type=bool, default=True, help='Morphometric data', dest='mor')
    parser.add_argument('-c', '--con', type=bool, default=False, help='Connectome data', dest='con')
    parser.add_argument('-e', '--european', type=bool, default=True, help='4k European GPS', dest='european')
    parser.add_argument('-me', '--multi-ethnic', type=bool, default=False, help='8k Multi-ethnic GPS', dest='multi_ethnic')
    return parser.parse_args()

def load_files(args):
    print('=====Start Importing Files=====')
    # Import connectome files
    if args.con:
        brain = pd.read_csv('/DIR/con_ct_merge.csv', header=0)
        brain['subjectkey'] = brain['subjectkey'].astype(str)[5:]

    # Import morphometric files
    elif args.mor:
        brain = pd.read_csv('/DIR/mor_merge.csv', header=0)
        brain['subjectkey'] = brain['subjectkey'].astype(str)[5:]

    else:
        print("No brain data is selected!")

    # Import gps
    start = 0
    end = 0
    # Import gps - 4k
    if args.european:
        gps = pd.read_csv('/DIR/gps_4000.csv', header=0)
        gps['subjectkey'] = gps['KEY'].astype(str)[4:]
        start = 1
        end = 27

    # Import gps - 8k
    elif args.multi_ethnic
        gps = pd.read_csv('/DIR/gps_8000.csv', header=0)
        gps['subjectkey'] = gps['FID'].astype(str).split("_")[2]
        start = 2
        end = 28

    else:
        print("No GPS data is selected!")

    return brain, gps, start, end

if __name__ == '__main__':
    args = get_args()
    brain, gps, start, end = load_files(args)

    # get only brain brain
    imp = Imputer(missing_values = np.nan, strategy = 'mean')
    X = brain.iloc[:, 1:]
    X = imp.fit_transform(X.values)

    # Do linear regression for each GPS
    print('=====Start Linear Regression=====')
    count = 1
    for target in gps.iloc[:,start:end].columns:
        print('[{}] {}'.format(count, target))
        y = gps[target]
        y.values.ravel()
        result = []
        
        length = len(X.columns)
        for col in range(length):
            x = X[:,col]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
            result.append([brain.columns[col+1], slope, intercept, r_value, p_value, std_err])

        print('=====Linear Regression is Successively  Done=====')
        scipy_result = pd.DataFrame(result, columns=['label', 'slope', 'intercept', 'r_value', 'p_value', 'std_err'])
        scipy_result.to_csv('_LR_result/brain_'+target+'_LR.csv', index=False)
        print('======The csv File is Generated=====')
