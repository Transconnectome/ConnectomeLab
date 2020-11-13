import pandas as pd 
import numpy as np

######### file specific constants #########
# idP: IdeationPassive, idA: IdeationActive, att: Attempt
test_file = {
    'idP' : "SuicidalideationPassive_test_imputed.csv",
    'idA' : "SuicidalideationActive_test_imputed.csv",
    'att' : "SuicideAttempt_test_imputed.csv",
    'ideation': "Suicidalideation_test_imputed.csv",
    'all': "Suicide_all_test_imputed.csv"
}
train_file = {
    'idP' : "SuicidalideationPassive_train_imputed.csv",
    'idA' : "SuicidalideationActive_train_imputed.csv",
    'att' : "SuicideAttempt_train_imputed.csv",
    'ideation': "Suicidalideation_train_imputed.csv",
    'all': "Suicide_all_train_imputed.csv"
}

# Suicide columns
sui_index = {  # Ideation Passive(107), Ideation Active(108), Attempt(112)
    'idP': 'SuicidalideationPassive',
    'idA': 'SuicidalideationActive',
    'att': 'SuicideAttempt',
    'ideation': 'Suicidalideation',
    'all': 'Suicide_all'
}
# Column numbers for each models
demo = ['age', 'sex', 'abcd_site', 'married', 'high.educ']
gps = (1, 26)
gps_sig = { 
    'idP' : [1, 5, 9, 11, 15, 23], # GENERAL HAPPINESS_MEANINGFUL, INSOMNIA, RISK4PC, SMOKER, CP, ADHD
    'idA' : [15, 16], # ADHD, ASD
    'att' : [3, 10, 17, 22, 24], # GENERAL HAPPINESS, SCZ, DEPRESSION, RISKTOL, EA
    'ideation' : [1, 5, 9, 11, 15, 16, 23],
    'all': [1, 3, 5, 9, 10, 11, 15, 16, 17, 22, 23, 24]
}
pheno = [31]+[i for i in range(38, 98)] + [i for i in range(135, 139)] # add family

fam = ['fes_q1', 'fes_q2', 'fes_q3', 'fes_q4', 'fes_q5', 'fes_q6', 'fes_q7', 'fes_q8', 'fes_q9']

pheno_part = [i for i in range(57, 89)] # CBCL and ELS

def load_data(args):
    print('Start Importing Files...')

    sui_type = args.type
    
    # import files
    test_set = pd.read_csv(test_file[sui_type], header=0)
    train_set = pd.read_csv(train_file[sui_type], header=0)

    y_train = train_set[sui_index[sui_type]]
    y_test = test_set[sui_index[sui_type]]

    if args.demo: # this is always true
        X_train = train_set[demo]
        X_test = test_set[demo]
    
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
    
    if args.fam:
        fam_train = train_set[fam]
        fam_test = test_set[fam]
        X_train = pd.concat([X_train, fam_train], axis=1)
        X_test = pd.concat([X_test, fam_test], axis=1)
    
    if args.pheno_p:
        phenop_train = train_set.iloc[:, pheno_part]
        phenop_test = test_set.iloc[:, pheno_part]
        X_train = pd.concat([X_train, phenop_train], axis=1)
        X_test = pd.concat([X_test, phenop_test], axis=1)

    print(f'train X size: {len(X_train)}, train y size: {len(y_train)}')
    print(f'test X size: {len(X_test)}, test y size: {len(y_test)}')


    return X_train, y_train, X_test, y_test

def remove_nan(X, y):
    X = X.dropna()
    y = y[X.index]
    
    print(f'After Dropping NAs: {len(X)}')

    return X, y

def fill_nan(X, y):
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())
    
    return X, y

def under_sampling(X, y):
    count = y.value_counts()
    print('Before under sampling')
    print(f'# of case: {count[1]} \n# of control: {count[0]}')
    
    Xy = pd.concat([X, y], axis=1)
    
    case = Xy[Xy[y.name]==1]
    control = Xy[Xy[y.name]==0]
    
    print('After under sampling')
    if len(case) < len(control):
        control_under = control.sample(count[1], random_state=123)
        combine_under = pd.concat([control_under, case], axis=0)
        print(f'# of case: {count[1]} \n# of control: {len(control_under)}')
    else:
        case_under = case.sample(count[0], random_state=123)
        combine_under = pd.concat([case_under, control], axis=0)
        print(f'# of case: {len(case_under)} \n# of control: {count[0]}')
    
    y_new = combine_under[y.name]
    X_new = combine_under.drop(columns=y.name)
    
    return X_new, y_new

