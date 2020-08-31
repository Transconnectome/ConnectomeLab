#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 SKX nodes
#----------------------------------------------------
​
#SBATCH -J ADHD_PCA           # Job name
#SBATCH -o ADHD_PCA.o%j       # Name of stdout output file
#SBATCH -e ADHD_PCA.e%j       # Name of stderr error file
#SBATCH -p skx-normal     # Queue (partition) name / dev도 있고 skx-normal, long 같은 경우는 knl
#SBATCH -N 1               # Total # of nodes (must be 1 for serial) > qlimits 라고 커맨드에 치면 limits 볼 수 있음
#SBATCH -n 1               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 48:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=dhkdgmlghks@snu.ac.kr
#SBATCH --mail-type=all    # Send email at begin and end of job
​
​
# Other commands must follśw all #SBATCH directives...
cd /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA #stdout/ err output file goes in! WORKSPACE
module load Rstats
pwd
date
​
​
# Launch serial code...
​
Rscript /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA/PRSice.R \
--prsice /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA/PRSice_linux \
--dir /work/07406/yoonbal/stampede2/PRSice2/ADH_PCAD \
--base /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA/PGC_ADHD_EA_2.txt \
--target /work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed \
--A1 A1 \
--A2 A2 \
--bp BP \
--snp SNP \
--pvalue P \
--no-default \
--stat OR \
--no-regress \
--score avg \
--model add \
--extract /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA/ADHD.valid \
--maf 0.01 \
--info 0.9 \
--cov /work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed_PRSice2_pca.eigenvec \
--cov-col @PC[1-10] \
--ld-maf 0.05 \
--thread max \
--bar-levels 0.00000005,0.0000005,0.000005,0.00005,0.0005,0.005,0.05,1 \
--out /work/07406/yoonbal/stampede2/PRSice2/ADHD_PCA
​
 # dev 경우 ibrun 했고 아닌경우는 Rscript file명.R
​
# ---------------------------------------------------