
# load gps_merged
gps <- read.csv("gps\\gps_abcd_prsice2_pca_scaled.csv", header=T)

# load morphometric data
mor <- read.csv("brain_data\\mor_merge.csv", header=T)
mor$KEY = sub("_", "", mor$subjectkey) # set KEY to merge

# merge gps with morphometric data
gps.mor <- merge(gps, mor, by='KEY')
str(gps.mor)

# where is start of mor
names(gps.mor)[42]

# test
length(gps.mor)
i=42

glm.re <- glm(CP~gps.mor[,i], data=gps.mor, family=gaussian())
cff <- coef(summary(glm.re))
cff
brain <- c(brain, colnames(gps.mor)[i])
brain
round(cff[2, 1], 5)
glm.cff <- c(glm.cff, round(cff[2, 1], 5))
glm.se <- c(glm.se, round(cff[2, 2], 5))
glm.p <- c(glm.p, round(cff[2, 4], 10))

glm.cff
glm.se
glm.p

# initialize all vector
brain <- vector()
glm.cff <- vector()
glm.se <- vector()
glm.p <- vector()

# glm with no covarites
for (i in 42:length(gps.mor)){
  glm.re <- glm(CP~gps.mor[,i], data=gps.mor, family=gaussian())
  cff <- coef(summary(glm.re))
  brain <- c(brain, colnames(gps.mor)[i])
  glm.cff <- c(glm.cff, round(cff[2, 1], 5))
  glm.se <- c(glm.se, round(cff[2, 2], 5))
  glm.p <- c(glm.p, round(cff[2, 4], 10))
}

head(brain)
head(glm.cff)
head(glm.se)
head(glm.p)

result <- data.frame(brain, glm.cff, glm.se, glm.p)
str(result)
colnames(result) = c("region", 'estimate', 'SE', 'P')

write.csv(result, "glm_mor_gps_CP.csv", quote = F)


for(i in 40:ncol(gps.mor)){
  glm.re <- glm(CP~gps.mor[,i], data=gps.mor, family=gaussian())
}

# save(gps.mor, file="gps_mor_merged.RData")
