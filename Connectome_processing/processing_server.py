import pandas as pd 
import numpy as np
import os
import argparse

# directory for file
data_dir = '/scratch/connectome/mrtrix_group_v2/'
save_dir = './' # This directory also contains the brain name files

# aparc+aseg
aparc = {
    'ad' : 'aparc+aseg_v2_AD.csv',
    'fa' : 'aparc+aseg_v2_FA.csv',
    'md' : 'aparc+aseg_v2_MD.csv',
    'rd' : 'aparc+aseg_v2_RD.csv',
    'count' : 'aparc+aseg_v2_count_v2.csv',
    'length' : 'aparc+aseg_v2_length_v2.csv',
}

# a2009s+aseg
a2009s = {
    'ad' : 'aparc.a2009s+aseg_v2_AD.csv',
    'fa' : 'aparc.a2009s+aseg_v2_FA.csv',
    'md' : 'aparc.a2009s+aseg_v2_MD.csv',
    'rd' : 'aparc.a2009s+aseg_v2_RD.csv',
    'count' : 'aparc.a2009s+aseg_v2_count_v2.csv',
    'length' : 'aparc.a2009s+aseg_v2_length_v2.csv',
}

row_num = {
    'aparc' : 84,
    'a2009s' : 164,
}

atlas = ['aparc', 'a2009s']
data_type = ['ad', 'fa', 'md', 'rd', 'count', 'length']

seg_files = {
    'aparc' : 'fs_default.txt',
    'a2009s' : 'fs_a2009s.txt'
}

def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--atlas', type=str, default='aparc', 
                        choices=atlas, dest='atlas', help='Choose Atlas')
    parser.add_argument('-t', '--type', type=str, default='count', 
                        choices=data_type, dest='type', help='Choose Type')
    return parser.parse_args()

def get_filenames(args):
    print('\nYour choice: {} + {}'.format(args.atlas, args.type))
    print('Getting file names...\n')
    fileend = aparc[args.type] if args.atlas == 'aparc' else a2009s[args.type]
    
    files = os.listdir(data_dir)
    my_files = [file for file in files if file.endswith(fileend)]

    print('# of subjects: {}'.format(len(my_files)))
    return my_files

def processing(file_names, args):
    length = row_num[args.atlas]

    print('Creating column names ...')
    seg_names = pd.read_table(save_dir+seg_files[args.atlas], sep='\s+', index_col=0)
    if args.atlas == 'aparc':
        seg = [name.replace(".", "-") for name in seg_names.iloc[:,0]]
    else: 
        seg = [name.replace("ctx", "") for name in seg_names.iloc[:,0]]
    
    col_names = []
    col_names.append('subjectkey')
    for row in range(length):
        for col in range(row+1, length):
            col_names.append('con_'+seg[row]+'_'+seg[col]+'_'+args.type)
    
    print('# of columns: {}'.format(len(col_names)))
    print('Done!\n')

    atlas = 'aparc' if args.atlas == 'aparc' else 'aparc_a2009s'
    filename = 'con_'+atlas+'_'+args.type+'.csv'

    print('Start processing data...')
    result = []
    cnt_row = 0
    for file in file_names:
        raw = pd.read_csv(data_dir+file, sep=' ', header=None)
        raw = raw.to_numpy()
        
        ut = raw[np.triu_indices(length, 1)]
        buf = [file.split('_')[0]] + list(ut)
        result.append(buf)
        cnt_row += 1
        if cnt_row%1000 == 0:
            print('Now processing... {}th'.format(cnt_row))
    print('# of triu_indies: {}'.format(len(result[0])))
    print('Done!\n')

    print('Start making pd.DataFrame...')
    result_all = pd.DataFrame(result, columns=col_names)
    print(result_all.head())

    print('Start making csv file...')
    result_all.to_csv(save_dir+filename, index=False)
    print('# of row: {}'.format(len(result_all)))


if __name__=='__main__':
    args = get_args()
    file_names = get_filenames(args)
    processing(file_names, args)
    print('All Clear!\n')

