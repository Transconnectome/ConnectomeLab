gps <- read.csv("gps_abcd_8k_norm.csv", header=T)

str(gps)

female <- gps$female == 1
male <- gps$female == 0

#WORRY
var.test(gps[female, 'WORRY'], gps[male, 'WORRY'])
t.test(gps[female, 'WORRY'], gps[male, 'WORRY'], paired=F, var.equal = T, conf.level = 0.95)

#CP
var.test(gps[female, 'CP'], gps[male, 'CP'])
t.test(gps[female, 'CP'], gps[male, 'CP'], paired=F, var.equal = T, conf.level = 0.95)

#EA
var.test(gps[female, 'EA'], gps[male, 'EA'])
t.test(gps[female, 'EA'], gps[male, 'EA'], paired=F, var.equal = T, conf.level = 0.95)

