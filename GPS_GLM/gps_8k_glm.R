gps <- read.csv("gps\\ABCD_all_Pt1_score_new_version.csv")
str(gps)
cli <- read.csv("clinic\\abcd_demographic_data.csv", header=T)
str(cli)
cli$KEY = sub("_", "", cli$subjectkey)
str(cli)
gps_merged <- merge(cli, gps, by='KEY')
str(gps_merged)
write.csv(gps_merged, 'gps\\gps_abcd_8k_new.csv', quote=F, row.names=F)

mor <- read.csv("brain_data\\mor_merge.csv", header=T)
mor$KEY = sub("_", "", mor$subjectkey)

gps_glm <- glm(race.ethnicity~CP+age+female+abcd_site, data=gps_merged, family=gaussian())
str(gps_glm)

summary(gps_glm)
save(gps_merged, mor, file="gps_8k_glm.RData")
