import os
import pandas as pd
from bioinfokit import visuz
import re

# working directory: /content/drive/My Drive/ConnectomeLab/GLM_results

# Get file names
file_names = os.listdir('./gps_mor')

# Make unique list
glm = pd.read_csv(file_names[0], header=0)
glm = glm.drop(columns = 'Unnamed: 0')

unique_AREA = []
unique_VOL = []
unique_MC = []
unique_THICK = []
unique_SUB = []
duplicated_AREA = []
duplicated_VOL = []
duplicated_MC = []
duplicated_THICK = []
duplicated_SUB = []

for i in range(len(glm)):
    name = str(glm.iloc[i, 0])
    name_no_digits = re.sub('\d', '', name)
    if '_area' in name:
        if not name_no_digits in unique_AREA:
            unique_AREA.append(name_no_digits)
        else:
            duplicated_AREA.append(name)
    elif '_volume' in name:
        if not name_no_digits in unique_VOL:
            unique_VOL.append(name_no_digits)
        else:
            duplicated_VOL.append(name)
    elif '_meancurv' in name:
        if not name_no_digits in unique_MC:
            unique_MC.append(name_no_digits)
        else:
            duplicated_MC.append(name)
    elif '_thickness' in name:
        if not name_no_digits in unique_THICK:
            unique_THICK.append(name_no_digits)
        else:
            duplicated_THICK.append(name)
    else:
        if not name_no_digits in unique_SUB:
            unique_SUB.append(name_no_digits)
        else:
            duplicated_SUB.append(name)
        
print('area: ', len(duplicated_AREA))
print('vol: ', len(duplicated_VOL))
print('mean curv: ', len(duplicated_MC))
print('thickness: ', len(duplicated_THICK))
print('none: ', len(duplicated_SUB))


for file in file_names:
    AREA = pd.DataFrame()
    VOLUME = pd.DataFrame()
    MEANCURV = pd.DataFrame()
    THICK = pd.DataFrame()
    SUB = pd.DataFrame()

    glm = pd.read_csv('./gps_mor/'+file, header=0)

    for i in range(len(glm)):
        name = str(df.iloc[i, 0])
        if '_area' in name and not name in duplicated_AREA:
            AREA = AREA.append(df.iloc[i, :], ignore_index=True)
        elif '_volume' in name and not name in duplicated_VOL:
            VOLUME = VOLUME.append(df.iloc[i, :], ignore_index=True)
        elif '_meancurv' in name and not name in duplicated_MC:
            MEANCURV = MEANCURV.append(df.iloc[i, :], ignore_index=True)
        elif '_thickness' in name and not name in duplicated_THICK:
            THICK = THICK.append(df.iloc[i, :], ignore_index=True)
        elif not name in duplicated_NONE:
            NONE = NONE.append(df.iloc[i, :], ignore_index=True)

    AREA['label'] = 'area'
    VOLUME['label'] = 'volume'
    MEANCURV['label'] = 'mean_curv'
    THICK['label'] = 'thickness'
    NONE['label'] = 'sub_cortical'

    ALL = pd.DataFrame()
    ALL = ALL.append(AREA, ignore_index=True)
    ALL = ALL.append(VOLUME, ignore_index=True)
    ALL = ALL.append(MEANCURV, ignore_index=True)
    ALL = ALL.append(THICK, ignore_index=True)
    ALL = ALL.append(NONE, ignore_index=True)

    print(file_names[0])
    print(len(ALL))
    visuz.marker.mhat(df=ALL, axlabelfontname='DejaVu Sans', axxlabel='CP-morphometric', 
                figname= './plots/MTP_CP_mor',
                pv='p_brain', chr='label', show = False, gwas_sign_line=True, color=("#f55354", "#f59b25", "#7fc638", "#754100", "#586fab"),  gwasp=0.05/len(ALL))
