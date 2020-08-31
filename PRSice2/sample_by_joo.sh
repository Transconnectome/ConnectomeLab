#! /bin/bash
#MSUB -A b1042
#MSUB -l nodes=4:ppn=12
#MSUB -q genomics
#MSUB -N "PRSice_test61"
#MSUB -l walltime=24:00:00
​
​
###    --A1                    Column header containing allele 1 (effective allele)                            Default: A1\n  (=MTAG format is the same)
###    --A2                    Column header containing allele 2 (non-effective allele)                            Default: A2\n
​
cd $PBS_O_WOKRDIR
​
module load R
​
Rscript /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/PRSice_linux_2/PRSice.R \
--prsice /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/PRSice_linux_2/PRSice_linux \
--dir /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/ \
--base /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/felix_PCOS_ALL_030620151_FreqLowerThan015e3_formattedforPRsice_ver3.tbl \
--target /projects/b1074/data/E3_Imputed_V2/Data/Best_Guess_PLINK/chr#.hard_geno.emerge_ids.consented.merged.plink \
--A1 Allele1 \
--A2 Allele2 \
--beta \
--snp SNP \
--pvalue Pvalue \
--se StdErr \
--stat Effect \
--clump-kb 500 \
--clump-p 1.000000 \
--clump-r2 0.2 \
--no-regress \
--score sum \
--model add \
--info 0.9 \
--maf 0.05 \
--ld-maf 0.05 \
--maf-base Freq1,0.05 \
--fastscore \
--bar-levels 0.00000005,0.0000005,0.000005,0.00005,0.0005,0.005,0.05,1 \
--thread max \
--exclude /projects/b1074/analysis/PCOS/E3_Variant_InfoScore/e3_duplicative_meanR2_less_than_0_5.snplist \
--out /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/Results_Feb2019/Feb2019_E3ver2_61ndtry_UpgradedPRS23_r2_02_sum_ALLmaf005