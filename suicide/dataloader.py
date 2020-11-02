import pandas as pd 
import numpy as np

######### file specific constants #########
# idP: IdeationPassive, idA: IdeationActive, att: Attempt
test_file = {
    'idP' : "test_train_set/SuicidalideationPassive_test.csv",
    'idA' : "test_train_set/SuicidalideationActive_test.csv",
    'att' : "test_train_set/SuicideAttempt_test.csv"
}
train_file = {
    'idP' : "test_train_set/SuicidalideationPassive_train.csv",
    'idA' : "test_train_set/SuicidalideationActive_train.csv",
    'att' : "test_train_set/SuicideAttempt_train.csv"
}
# Suicide columns
sui_index = {  # Ideation Passive(107), Ideation Active(108), Attempt(112)
    'idP': 107,
    'idA': 108,
    'att': 112
}
sui_columns = ['SuicidalideationPassive.x', 'SuicidalideationActive.x', 'SuicideAttempt.x']

# Column numbers for each models
demo = [27, 28, 30, 32, 33]
ksad = (98, 139) # Must Exclude Suicide
gps = (1, 26)
gps_sig = { 
    'idP' : [1, 5, 9, 11, 15, 23], # GENERAL HAPPINESS_MEANINGFUL, INSOMNIA, RISK4PC, SMOKER, CP, ADHD
    'idA' : [15, 16], # ADHD, ASD
    'att' : [3, 10, 17, 22, 24] # GENERAL HAPPINESS, SCZ, DEPRESSION, RISKTOL, EA
}
pheno = [i for i in range(36, 98)] + [i for i in range(140, 144)]

def load_data(args):
    print('Start Importing Files...')

    sui_type = args.type
    ######### Make X and y #########
    # import files
    test_set = pd.read_csv(test_file[sui_type], header=0)
    train_set = pd.read_csv(train_file[sui_type], header=0)

    y_train = train_set.iloc[:, sui_index[sui_type]]
    y_test = test_set.iloc[:, sui_index[sui_type]]

    if args.demo: # this is always true
        X_train = train_set.iloc[:, demo]
        X_test = test_set.iloc[:, demo]
    
    if args.ksad:
        ksad_wo_suicide_train = train_set.iloc[:, ksad[0]:ksad[1]+1].drop(columns = sui_columns)
        ksad_wo_suicide_test = test_set.iloc[:, ksad[0]:ksad[1]+1].drop(columns = sui_columns)
        X_train = pd.concat([X_train, ksad_wo_suicide_train], axis=1)
        X_test = pd.concat([X_test, ksad_wo_suicide_test], axis=1)

    if args.gps and args.gps_sig:
        print('GPS and SIGNIFICANT GPS cannot be true at the same time')
        print('Please close this program')

    if args.gps:
        gps_train = train_set.iloc[:, gps[0]:gps[1]+1]
        gps_test = test_set.iloc[:, gps[0]:gps[1]+1]
        X_train = pd.concat([X_train, gps_train], axis=1)
        X_test = pd.concat([X_test, gps_test], axis=1)

    elif args.gps_sig:
        print(train_set.columns[gps_sig[sui_type]])
        gps_sig_train = train_set.iloc[:, gps_sig[sui_type]]
        gps_sig_test = test_set.iloc[:, gps_sig[sui_type]]
        X_train = pd.concat([X_train, gps_sig_train], axis=1)
        X_test = pd.concat([X_test, gps_sig_test], axis=1)

    if args.pheno:
        pheno_train = train_set.iloc[:, pheno]
        pheno_test = test_set.iloc[:, pheno]
        X_train = pd.concat([X_train, pheno_train], axis=1)
        X_test = pd.concat([X_test, pheno_test], axis=1)

    print(f'train X size: {len(X_train)}, train y size: {len(y_train)}')
    print(f'test X size: {len(X_test)}, test y size: {len(y_test)}')
    # Drop NA
    X_train = X_train.dropna()
    X_test = X_test.dropna()
    y_train = y_train[X_train.index]
    y_test = y_test[X_test.index]

    print('\n')
    print('After Dropping NAs')
    print(f'train X size: {len(X_train)}, train y size: {len(y_train)}')
    print(f'test X size: {len(X_test)}, test y size: {len(y_test)}')
    print('\n')

    X_train = X_train.to_numpy()
    y_train = y_train.to_numpy().ravel()
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy().ravel()

    return X_train, y_train, X_test, y_test
