[Reference code for Team3] PheWAS sample code 

## PCOS PheWAS with 55th PRS -  under age 14 filtered
## sex-stratified within EU population  + MultiEthnic

library("PheWAS")

# call phenotype/cov
phecode_unique <- read.table("/projects/b1074/analysis/PCOS/PhenoPrep_phecode_9and10_unique_11052018.txt", header=TRUE, check.names=TRUE) #phenotype file - premade 
cov <- read.csv("/projects/b1074/analysis/PCOS/chr1-22.plink_pca.e123_imputation_sample_manifest.csv", header=TRUE)[,-c(2,3,11:16)] #genotype pca file 
names(cov)[1] <- "id"
caucasian <- subset(cov$id, cov$genetic_ancestry_race=="caucasian")
cov <- cov[,-4]	#remove 'RACE' column in cov 
cov <- subset(cov, cov$id %in% caucasian)
related <- read.table("/projects/b1074/data/E3_Imputed/Information/suspect_IBD_samples_to_remove", header=FALSE)
phecode_unique <- phecode_unique[!phecode_unique$ID %in% related$V1,] #81748 -> 81402


# Call PRS with different p-values 
prs <- read.table("/projects/b1074/analysis/PCOS/PRSriskscore_byPRsice/Results_Oct2018/Results_Oct2018_55ndtry_MTAGver5_r2_01_sum_info09_ALLmaf005_R5_05.all.score", header=TRUE, check.names=T)[,-c(1,3)]
names(prs)[1] <- "id"
prs <- prs[!prs$id %in% related$V1,]   
prsEAAA_5e6 <- prs[,c(1,2)]
prsEAAA_5e3 <- prs[,c(1,5)]
prsEAAA_5e2 <- prs[,c(1,6)]
prsEAAA_all <- prs[,c(1,7)]
names(prsEAAA_5e6)[2] <- "PRS"
names(prsEAAA_5e3)[2] <- "PRS"
names(prsEAAA_5e2)[2] <- "PRS"
names(prsEAAA_all)[2] <- "PRS"

prs <- prs[prs$id %in% caucasian,] # only EU 
prs_5e6 <- prs[,c(1,2)]
prs_5e3 <- prs[,c(1,5)]
prs_5e2 <- prs[,c(1,6)]
prs_all <- prs[,c(1,7)]
names(prs_5e6)[2] <- "PRS"
names(prs_5e3)[2] <- "PRS"
names(prs_5e2)[2] <- "PRS"
names(prs_all)[2] <- "PRS"



# phenotype 
phecode_unique$Phecode <- as.character(phecode_unique$Phecode)
phecode_unique$count <- 1
phenotype <- createPhewasTable(phecode_unique, translate=F, min.code.count=1)
names(phenotype)[1] <- "id"
phenotypeEAAA <- phenotype
phenotype <- subset(phenotype, phenotype$id %in% caucasian)

# gender specific 
female <- subset(cov$id, cov$sex2=="female")
male <- subset(cov$id, cov$sex2=="male")
phenotype_male <- subset(phenotype, phenotype$id %in% male)	# set phenotype
phenotype_female <- subset(phenotype, phenotype$id %in% female)
cov <- cov[,-2]	#remove 'gender' column in cov 
covEAAA <- cov 
cov_male <- subset(cov, cov$id %in% male)	# set covariate 
cov_female <- subset(cov, cov$id %in% female)
prs_male <- subset(prs, prs$id %in% male)	# set genotype (prs)
prs_male_5e6 <- prs_male[,c(1,3)]
prs_male_5e3 <- prs_male[,c(1,3)]
prs_male_5e2 <- prs_male[,c(1,4)]
prs_male_all <- prs_male[,c(1,5)]
prs_female <- subset(prs, prs$id %in% female)
prs_female_5e6 <- prs_female[,c(1,3)]
prs_female_5e3 <- prs_female[,c(1,3)]
prs_female_5e2 <- prs_female[,c(1,4)]
prs_female_all <- prs_female[,c(1,5)]



### 1. ALL (both sexes)

# 1-1. PheWAS full - EU+AA ALL


results_1 <- phewas(phenotypeEAAA, predictors=prsEAAA_5e6, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_2 <- phewas(phenotypeEAAA, predictors=prsEAAA_5e3, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_3 <- phewas(phenotypeEAAA, predictors=prsEAAA_5e2, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_4 <- phewas(phenotypeEAAA, predictors=prsEAAA_all, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)

# TEST TWO DIFFERENT METHODS FOR ANNOTATION 
results1 <- addPhecodeInfo(results_1)
results2 <- addPhecodeInfo(results_2)
results3 <- addPhecodeInfo(results_3)
results4 <- addPhecodeInfo(results_4)

write.csv(results1, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e6.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results2, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e3.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results3, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e2.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results4, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_ALL.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)

results_a_sig <- results1[!is.na(results1$p),]
results_a_sig <- results_a_sig[(results_a_sig$p)<0.05,]
results_b_sig <- results2[!is.na(results2$p),]
results_b_sig <- results_b_sig[(results_b_sig$p)<0.05,]
results_c_sig <- results3[!is.na(results3$p),]
results_c_sig <- results_c_sig[(results_c_sig$p)<0.05,]
results_d_sig <- results4[!is.na(results4$p),]
results_d_sig <- results_d_sig[(results_d_sig$p)<0.05,]

write.csv(results_a_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e6.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_b_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e3.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_c_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e2.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_d_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_MultiEthnic_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_ALL.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")




# 1-2. PheWAS FULL - case=30  - EU Only 
results_1 <- phewas(phenotype, predictors=prs_5e6, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_2 <- phewas(phenotype, predictors=prs_5e3, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_3 <- phewas(phenotype, predictors=prs_5e2, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)
results_4 <- phewas(phenotype, predictors=prs_all, covariates=cov, cores=2, additive.genotypes=FALSE, significance.threshold=c("p-value","bonferroni","fdr"), min.record=30)

# TEST TWO DIFFERENT METHODS FOR ANNOTATION 
results1 <- addPhecodeInfo(results_1)
results2 <- addPhecodeInfo(results_2)
results3 <- addPhecodeInfo(results_3)
results4 <- addPhecodeInfo(results_4)

write.csv(results1, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e6.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results2, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e3.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results3, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_5e2.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)
write.csv(results4, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_full_Age14_Filtered_ALL.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE)

results_a_sig <- results1[!is.na(results1$p),]
results_a_sig <- results_a_sig[(results_a_sig$p)<0.05,]
results_b_sig <- results2[!is.na(results2$p),]
results_b_sig <- results_b_sig[(results_b_sig$p)<0.05,]
results_c_sig <- results3[!is.na(results3$p),]
results_c_sig <- results_c_sig[(results_c_sig$p)<0.05,]
results_d_sig <- results4[!is.na(results4$p),]
results_d_sig <- results_d_sig[(results_d_sig$p)<0.05,]

write.csv(results_a_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e6.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_b_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e3.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_c_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_5e2.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")
write.csv(results_d_sig, file="/projects/b1074/analysis/PCOS/PheWAS_Oct2018/PCOSphewas_12032018_with55ndPRS_EUonly_CovSitesPC14_FreqLowerThan015e3_r2_01_sig_Age14_Filtered_ALL.csv", na="NA", col.names=TRUE, row.names=FALSE, quote=TRUE, sep="\t")

