covars = c("sex", "race.ethnicity", "high.educ", "income", "married", "abcd_site", "age", "vol", "height", "weight", "BMI")
locs.sex = grep("sex", covars)
locs.vol = grep("vol", covars)
if(cov.sex == T & cov.vol == T){
  covs = covars
} else if(cov.sex == F & cov.vol == T){
  covs = covars[-locs.sex]
} else if(cov.sex == T & cov.vol == F){
  covs = covars[-locs.vol]
} else if(cov.sex == F & cov.vol == F){
  covs = covars[-c(locs.sex, locs.vol)]
} else {
  covs = covars
}

forms = paste(names(df[7:37]), '~ pred.sex.2') #e.g.)CBCL ~ pred.sex.1
for(i in 1:length(covars)){
  forms = paste(forms, '+', covars[i]) ##e.g.)CBCL ~ pred.sex.1 + covariate
}

for(i in 1:length(forms)){ #n=31(CBCL, NIH, ELS)
  form = as.formula(forms[i])
  temp.glm <- glm(formula = form, data = temp.df)
  name[i] <- temp.names[i]
  temp.coeff[i] <- round(temp.glm[[1]][2], 5)
  temp.se[i] <- round(coef(summary(temp.glm))[2, 2], 5)
  temp.p[i] <- round(coef(summary(temp.glm))[2, 4], 10)
}

# https://stackoverflow.com/questions/23838937/extract-pvalue-from-glm