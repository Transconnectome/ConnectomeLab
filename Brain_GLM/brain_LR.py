# Brain Linear Regression
# You can specify brain/GPS data for input
# default is morphometric&4kGPS

import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import Imputer
from scipy import stats

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Conducting Linear Regression on GPS and Brain', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--brain', type=str, default='mor', choices=['mor', 'con'], help='Morphometric data', dest='brain')
    parser.add_argument('-g', '--gps', type=str, default='4k', choices=['4k', '8k'], help='Connectome data', dest='gps')

    return parser.parse_args()

def load_files(args):
    print('=====Start Importing Files=====')
    # Import connectome files
    if args.brain == 'con':
        brain = pd.read_csv('/home/ubuntu/SEOYOON/BRAIN/Data/con_ct_merge.csv', header=0)
        brain['subjectkey'] = brain['subjectkey'].str.split("_").str[1]

    # Import morphometric files
    elif args.brain == 'mor':
        brain = pd.read_csv('/home/ubuntu/SEOYOON/BRAIN/Data/mor_merge.csv', header=0)
        brain['subjectkey'] = brain['subjectkey'].str.split("_").str[1]
        print(brain.loc[1,'subjectkey'])

    else:
        print("No brain data is selected!")

    # Import gps
    # Import gps - 4k
    if args.gps == '4k':
        gps = pd.read_csv('/home/ubuntu/SEOYOON/GPS/GPS_TOTAL_v2_raw.csv', header=0)
        gps['subjectkey'] = gps['KEY'].str[4:]
        print(gps.loc[1,'subjectkey'])

    # Import gps - 8k
    elif args.gps == '8k':
        gps = pd.read_csv('/home/ubuntu/SEOYOON/GPS/ABCD_all_Pt1_score.csv', header=0)
        gps['subjectkey'] = gps['FID'].str.split("_").str[2]
        gps.drop(columns='IID')

    else:
        print("No GPS data is selected!")

    print('Merging two files...')
    merged = pd.merge(gps, brain, on='subjectkey', how='inner')
    print('Number of Subjects: {}'.format(len(merged)))

    gps_list = gps.columns[1:27]
    print("GPS list: ", gps_list)
        
    # [0:27] GPS and subject keys
    # [28: ] brain data

    return merged, gps_list

if __name__ == '__main__':
    args = get_args()
    merged, gps_list = load_files(args)

    # get only brain brain
    imp = Imputer(missing_values = np.nan, strategy = 'mean')
    X = merged.iloc[:, 28:]
    X = imp.fit_transform(X.values)

    # Do linear regression for each GPS
    print('=====Start Linear Regression=====')
    count = 1
    for target in gps_list:
        print('[{}] {}'.format(count, target))
        y = merged[target]
        y.values.ravel()
        result = []
        
        length = len(X.columns)
        for col in range(length):
            x = X[:,col]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
            result.append([merged.columns[col+28], p_value, r_value, slope, intercept, std_err])

        print('=====Linear Regression is Successively  Done=====')
        scipy_result = pd.DataFrame(result, columns=['label', 'p_value', 'r_value', 'slope', 'intercept', 'std_err'])
        file_name = '/home/ubuntu/SEOYOON/BRAIN/LinearRegression/'+args.brain+'_'+args.gps+'_'+target+'_LR.csv'
        scipy_result.to_csv(file_name, index=False)
        print('Created: {}'.format(file_name))
