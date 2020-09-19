cli <- read.csv("clinic\\abcd_demographic_data.csv", header=T)

gps <- read.csv("gps\\GPS_TOTAL_v2_norm.csv", header=T)

str(cli)
str(gps)

cli$KEY <- sub("_", "", cli$subjectkey)
str(cli)

merged <- merge(cli, gps, by='KEY')
str(merged)

write.csv(merged, "gps\\gps_abcd_4k_norm.csv", quote = F, row.names=F)

female <- merged$female==1
male <- merged$female ==0

for (i in 14:39){
  print(colnames(merged)[i])
  print(var.test(merged[female, i], merged[male, i]))
  print(t.test(merged[female, i], merged[male, i], paired=F, var.equal = T, conf.level = 0.95))
}
