import pandas as pd 
import numpy as np
import os
import argparse

# directory for file
data_dir = 'C:\\Users\\SEOYOON_MOON\\Desktop\\ConnectomeLab\\connectome_data\\connectome_raw\\'

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
    'a2009s' : 164
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
    # parser.add_argument('-sa','--select_all', type=bool, default=False, dest=all, help='Select All')
    return parser.parse_args()

def get_filenames(args):
    print('\nYour choice: {} + {}'.format(args.atlas, args.type))
    fileend = aparc[args.type] if args.atlas == 'aparc' else a2009s[args.type]
    
    files = os.listdir(data_dir)
    my_files = [file for file in files if file.endswith(fileend)]

    return my_files

def processing(file_names, args):
    length = row_num[args.atlas]

    seg_names = pd.read_table(data_dir+seg_files[args.atlas], sep='\s+', index_col=0) 
    col_names = []
    col_names.append('subjectkey')
    for row in range(length):
        for col in range(row+1, length):
            # I should modify this part: numbers should be names in the brain
            col_names.append('con_'+seg_names.iloc[row, 0]+'_'+seg_names.iloc[col, 0]+'_'+args.type)

    atlas = 'aparc' if args.atlas == 'aparc' else 'aparc_a2009s'
    filename = 'con_'+atlas+'_'+args.type+'.csv'

    result = pd.DataFrame(columns=col_names)
    cnt_row = 0
    for file in file_names:
        raw = pd.read_csv(data_dir+file, sep=' ', header=None)

        buf = {}
        buf['subjectkey'] = file.split('_')[0]

        cnt = 1
        for row in range(length):
            for col in range(row+1, length):
                buf[col_names[cnt]] = raw.iloc[row, col]
                # buf.append(raw.iloc[row, col])
                cnt += 1

        print(buf['subjectkey'])
        result = pd.concat([result, pd.DataFrame(buf, index=[cnt_row])], ignore_index=True)
        cnt_row += 1

    print(result)
    result.to_csv(filename, index=False)

def processing_nparray(file_names, args):
    length = row_num[args.atlas]

    seg_names = pd.read_table(data_dir+seg_files[args.atlas], sep='\s+', index_col=0)
    if args.atlas == 'aparc':
        seg = [name.replace(".", "-") for name in seg_names.iloc[:,0]]
    else: 
        seg = [name.replace("ctx", "") for name in seg_names.iloc[:,0]]
    
    col_names = []
    col_names.append('subjectkey')
    for row in range(length):
        for col in range(row+1, length):
            col_names.append('con_'+seg[row]+'_'+seg[col]+'_'+args.type)

    atlas = 'aparc' if args.atlas == 'aparc' else 'aparc_a2009s'
    filename = 'con_'+atlas+'_'+args.type+'.csv'

    result = []
    cnt_row = 0
    for file in file_names:
        raw = pd.read_csv(data_dir+file, sep=' ', header=None)
        raw = raw.to_numpy()
        print('length of raw: {}'.format(len(raw)))
        
        ut = raw[np.triu_indices(length, 1)]
        buf = [file.split('_')[0]] + list(ut)
        # print(buf[0], len(buf))
        result.append(buf)
        cnt_row += 1

    result_all = pd.DataFrame(result, columns=col_names)
    print(result_all.head())
    result_all.to_csv(filename, index=False)


if __name__=='__main__':
    args = get_args()
    file_names = get_filenames(args)
    processing_nparray(file_names, args)

