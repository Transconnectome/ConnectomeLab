
#GPS: PRSice2(ethnically corrected)
#BRIN: morphometric

# Import GPS LIST
# GPS_LIST <- read.table("gps\\GPS_LIST.txt", sep='\n', header=F)

# Covariates
COV_LIST <- c('age', 'female', 'high.educ', 'income', 'abcd_site', 'height', 'weight', 'BMI') # should be checked
COVARS <- paste(COV_LIST, collapse=" + ")

# Import GPS data
GPS <- read.csv("gps\\gps_abcd_prsice2_pca_scaled.csv", header=T)

#Import BRAIN data
BRAIN <- read.csv("brain_data\\mor_merge.csv", header=T)
BRAIN$KEY = sub("_", "", BRAIN$subjectkey)

# Merge GPS and BRAIN
MERGED <- merge(GPS, BRAIN, by='KEY')


# where is start of BRAIN
names(MERGED)[42]
BRAIN_START = 42
BRAIN_END <- length(MERGED)
NUM_GPS <- length(GPS_LIST)


BETA_LIST <- c('Intercept', 'beta_brain')
P_LIST <- c('p_inter', 'p_value')
BETA_LIST_COV <- c('Intercept', 'beta_brain', paste0('beta_', COV_LIST))
P_LIST_COV <- c('p_inter', 'p_value', paste0('p_', COV_LIST))

# Excluding list
# EXCLUDE <- c('eTIV.', 'Mask.')
# EXCLUDE_LIST <- vector()
# print("Excluding 'eTIV.' and 'Mask'...")
# for (i in BRAIN_START:BRAIN_END){
#   for (name in EXCLUDE){
#     if (grepl(name, names(MERGED)[i])){
#       EXCLUDE_LIST <- c(EXCLUDE_LIST, names(MERGED)[i])
#       print(names(MERGED)[i])
#     }
#   }
# }


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
  for (i in BRAIN_START:BRAIN_END) {
    name <- names(MERGED)[i]
    brain <- c(brain, name)
    
    form <- paste(gps, '~', name)
    # NO covariates
    glm.re <-glm(as.formula(form), data = MERGED, family = gaussian())
    cff <- coef(summary(glm.re))
    glm.se <- c(glm.se, round(cff[2, 2], 5))
    glm.beta <- rbind.data.frame(glm.beta, cff[, 1])
    glm.p <- rbind.data.frame(glm.p, cff[, 4])
    
    form <- paste(form, '+', COVARS)
    # With covariates
    glm.re.cov <-glm(as.formula(form), data = MERGED, family = gaussian())
    cff.cov <- coef(summary(glm.re.cov))
    glm.se.cov <- c(glm.se.cov, round(cff.cov[2, 2], 5))
    glm.beta.cov <- rbind.data.frame(glm.beta.cov, cff.cov[, 1])
    glm.p.cov <- rbind.data.frame(glm.p.cov, cff.cov[, 4])
    
  }
  colnames(glm.beta) <- BETA_LIST
  colnames(glm.p) <- P_LIST
  result <- data.frame(brain, glm.beta, glm.p)
  result <- result[-which(duplicated(result$p_brain)),]
  FILE_NAME <- paste0('glm_gps_mor\\GLM_mor_', gps, '_prsice2_corrected.csv')
  write.csv(result, FILE_NAME, quote = F)
  
  colnames(glm.beta.cov) <- BETA_LIST_COV
  colnames(glm.p.cov) <- P_LIST_COV
  result.cov <- data.frame(brain, glm.beta.cov, glm.p.cov)
  result.cov <- result.cov[-which(duplicated(result.cov$p_brain)),]
  FILE_NAME.cov <- paste0('glm_gps_mor\\GLM_cov_mor_', gps, '_prsice2_corrected.csv')
  write.csv(result.cov, FILE_NAME.cov, quote = F)
}
