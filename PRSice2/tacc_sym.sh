#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script PRS using prsice
#   for TACC Stampede2 SKX nodes
#----------------------------------------------------
#SBATCH -J bipld2           # Job name
#SBATCH -o bipld2.o%j       # Name of stdout output file
#SBATCH -e bipld2.e%j       # Name of stderr error file
#SBATCH -p skx-dev     # Queue (partition) name / dev도 있고 skx-normal, long 같은 경우는 knl
#SBATCH -N 4               # Total # of nodes (must be 1 for serial) > qlimits 라고 커맨드에 치면 limits 볼 수 있음
#SBATCH -n 32               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=hk2874@nyu.edu
#SBATCH --mail-type=all    # Send email at begin and end of job
# Other commands must follśw all #SBATCH directives...
cd $/work/07406/yoonbal/stampede2/prsice_bip
module load R
Rscript /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/PRSice_linux_2/PRSice.R
--prsice /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/PRSice_linux_2/PRSice_linux
--dir /projects/b1074/analysis/PCOS/PRSriskscore_byPRsice
--base /work/07406/yoonbal/stampede2/ABCD_summarystats/PGC_BIP_2018
--target /work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed,/work/07406/yoonbal/stampede2/ABCD_genotype/ABCD_QCed.fam
# cols in sumstat: CHR	SNP	BP	A1	A2	FRQ_A_20352	FRQ_U_31358	INFO	OR	SE	P	ngt	Direction	HetISqt	HetDf	HetPVa	Nca	Nco	Neff
--snp SNP
--chr CHR
--bp BP
--A1 A1
--A2 A2
--stat OR
--pvalue P
--clump-kb 500
--clump-p 1.000000
--clump-r2 0.2
--no-regress
--score sum
--model add
--info 0.9
--maf 0.05
--ld-maf 0.05
--maf-base Freq1,0.01
--fastscore
--bar-levels 0.00000005,0.0000005,0.000005,0.00005,0.0005,0.005,0.05,1
--thread max
--exclude /projects/b1074/analysis/PCOS/E3_Variant_InfoScore/e3_duplicative_meanR2_less_than_0_5.snplist
--out /work/07406/yoonbal/stampede2/prsice_bip
--date
--bar-levels
--fastscore
--all-score