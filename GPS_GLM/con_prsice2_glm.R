
# FOR SERVER!
# GPS: PRSice2(ethnically corrected)
# BRIN: connectome

# Covariates
COV_LIST <- c('age', 'female', 'high.educ', 'income', 'abcd_site', 'height', 'weight', 'BMI') # should be checked
COVARS <- paste(COV_LIST, collapse=" + ")

# Import GPS data
GPS <- read.csv("/scratch/connectome/gps_con_glm/gps_data/gps_abcd_prsice2_pca_scaled.csv", header=T)

#Import BRAIN data
BRAIN <- read.csv("/scratch/connectome/processed/con_aparc_count.csv", header=T)

# Merge GPS and BRAIN
MERGED <- merge(GPS, BRAIN, by.x='KEY', by.y='subjectkey')

# where is start of BRAIN
print(names(MERGED)[41])

BRAIN_START <- 41

BRAIN_END <- length(MERGED)
NUM_SUBJECTS <- length(MERGED[[1]])

BETA_LIST <- c('Intercept', 'beta_brain')
P_LIST <- c('p_inter', 'p_brain')
BETA_LIST_COV <- c('Intercept', 'beta_brain', paste0('beta_', COV_LIST))
P_LIST_COV <- c('p_inter', 'p_brain', paste0('p_', COV_LIST))

# Filter some factors that values are all zero
ALL_ZERO_LIST <- vector()
print('Is there all-zero-valued region?')
for (i in 41:BRAIN_END){
  if(sum(MERGED[[i]]==0)==NUM_SUBJECTS){
    print(names(MERGED)[i])
    ALL_ZERO_LIST <- c(ALL_ZERO_LIST, names(MERGED)[i])
  }
}

for (gps in names(MERGED)[14:39]){
  print('----------')
  print(gps)
  # initialize all vector
  brain <- vector()
  
  glm.se <- vector()
  glm.beta <- data.frame()
  glm.p <- data.frame()
  
  glm.se.cov <- vector()
  glm.beta.cov <- data.frame()
  glm.p.cov <- data.frame()
  
  # DO GLM
  for (i in BRAIN_START:BRAIN_END){
    brain_region <- names(MERGED)[i]
    
    if (!(brain_region %in% ALL_ZERO_LIST)){
      brain <- c(brain, brain_region)
      
      form <- paste(gps, '~', brain_region)
      # NO covariates
      glm.re <- glm(as.formula(form), data=MERGED, family=gaussian())
      cff <- coef(summary(glm.re))
      glm.se <- c(glm.se, round(cff[2, 2], 5))
      glm.beta <- rbind.data.frame(glm.beta, cff[,1])
      glm.p <- rbind.data.frame(glm.p, cff[,4])
      
      form <- paste(form, '+', COVARS)
      # With covariates
      glm.re.cov <- glm(as.formula(form), data=MERGED, family=gaussian())
      cff.cov <- coef(summary(glm.re.cov))
      glm.se.cov <- c(glm.se.cov, round(cff.cov[2, 2], 5))
      glm.beta.cov <- rbind.data.frame(glm.beta.cov, cff.cov[,1])
      glm.p.cov <- rbind.data.frame(glm.p.cov, cff.cov[,4])
    }
    else {
      print(brain_region)
    }
  }
  # Save results
  colnames(glm.beta) <- BETA_LIST
  colnames(glm.p) <- P_LIST
  result <- data.frame(brain, glm.beta, glm.p)
  FILE_NAME <- paste0('GLM_con-cnt_', gps, '_prsice2.csv')
  write.csv(result, FILE_NAME, quote = F)
  
  colnames(glm.beta.cov) <- BETA_LIST_COV
  colnames(glm.p.cov) <- P_LIST_COV
  result.cov <- data.frame(brain, glm.beta.cov, glm.p.cov)
  FILE_NAME.cov <- paste0('GLM_cov_con-cnt_', gps, '_prsice2.csv')
  write.csv(result.cov, FILE_NAME.cov, quote = F)
}