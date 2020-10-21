# p value correction

FILES = list.files('.')
FILES

for (file in FILES){
  glm.result <- read.csv(file, header = T)
  P <- glm.result$p_brain
  BONF <- p.adjust(P, "bonferroni")
  FDR <- p.adjust(P, "fdr")
  
  corrected <- data.frame(glm.result$brain, P, BONF, FDR)
  
  splited <- unlist(strsplit(file, "_"))
  if ("cov" %in% splited){
    if (length(splited)==7){
      gps <- paste0(splited[4], splited[5])
    }
    else{
      gps <- splited[4]
    }
    save.name <- paste0("pvalue_corrected_cov_", gps, ".csv")
  }
  else{
    if (length(splited)==6){
      gps <- paste0(splited[3], splited[4])
    }
    else{
      gps <- splited[3]
    }
    save.name <- paste0("pvalue_corrected_", gps, ".csv")
  }
  
  write.csv(corrected, save.name, quote = F)
  
}
