#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script PRS using prsice
#   for TACC Stampede2 SKX nodes
#----------------------------------------------------
#SBATCH -J Prs07          # Job name
#SBATCH -o Prs07.o%j       # Name of stdout output file
#SBATCH -e Prs07.e%j       # Name of stderr error file
#SBATCH -p skx-dev    # Queue (partition) name / dev도 있고 skx-normal, long 같은 경우는 knl
#SBATCH -N 1               # Total # of nodes (must be 1 for serial) > qlimits 라고 커맨드에 치면 limits 볼 수 있음
#SBATCH -n 1               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=seoyoon5635@gmail.com
#SBATCH --mail-type=all    # Send email at begin and end of job
# Other commands must follśw all #SBATCH directives...
cd $/work/07406/yoonbal/stampede2/PRSice2/AD
module load Rstats
Rscript /work/07406/yoonbal/stampede2/PRSice2/PRSice.R \
--prsice /work/07406/yoonbal/stampede2/PRSice2/PRSice_linux \
--dir /work/07406/yoonbal/stampede2/PRSice2/AD \
--base /work/07406/yoonbal/stampede2/ABCD_summarystats/CNCR_AD_ver2.txt \
--target /work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed,/work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed.fam \
--chr CHR \
--A1 A1 \
--A2 A2 \
--bp BP \
--snp SNP \
--pvalue P \
--no-default \
--no-regress \
--score avg \
--model add \
--maf 0.01 \
--base-maf MAF:0.01 \
--fastscore \
--bar-levels 0.00000005,0.0000005,0.000005,0.00005,0.0005,0.005,0.05,1 \
--thread 28 \
--out /work/07406/yoonbal/stampede2/PRSice2/AD/AD \
--cov /work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed_PRSice2_pca.eigenvec \
--cov-col @PC[1-10]
# --extract /work/07406/yoonbal/stampede2/PRSice2/WORRY/iqout.valid
# cols in sumstat: CNR BP SNP A1 A2 EAF MAF Z BETA SE P N INFO_UKB
#--beta BETA \
# --info 0.9 \
# --extract /work/07406/yoonbal/stampede2/PRSice2/WORRY/WORRY.valid \