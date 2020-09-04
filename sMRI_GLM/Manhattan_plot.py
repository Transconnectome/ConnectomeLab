
import pandas as pd
import numpy as np
from bioinfokit import analys, visuz

gps=['AD', 'CANNABIS', 'IQ', 'CP', 'MDD', 'EA', 'ASP', 'RISKTOL', 'DRINK', 'INSOMNIA', 'GENERALHAPPINESS_HEALT', 'RISK4PC', 'ASD', 'SCZ', 'SMOKER', 'SNORING', 'GENERALHAPPINESS', 'WORRY', 'GENERALHAPPINESS_MEANINGFUL', 'PTSD', 'NEUROTICISM', 'ADHD', 'DEPRESSION', 'BMI', 'BIP', 'HAPPINESS']

count=1
labels = []
for target in gps:
    df=pd.read_csv('/home/ubuntu/SEOYOON/BRAIN_structural/StatsAnalysis/_LR_result/sMRI_'+target+'_LinearRegression_Pearson.csv', header = 0)
    if count ==1:
        labels = ["_".join(label.split("_")[1:2]) for label in df['label'].astype(str)]
    else:
        df['chr'] = labels

    print('[{}] {}'.format(count, target))
    visuz.marker.mhat(df=df, axlabelfontname='DejaVu Sans', axxlabel='sMRI Free Surfer ('+target+')', 
                      figname= '/home/ubuntu/SEOYOON/BRAIN_structural/StatsAnalysis/_Plots/mp1_'+target,
                      chr='chr',pv='p_value', show = False, color=("#d7d1c9", "#696464"), gwas_sign_line=True, gwasp=0.05/1186)
    count += 1
