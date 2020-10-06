[Reference code for Team3] Only for drawing phewas plot 

library("ggrepel")
test <- read.table("/Users/yooniejoo/Documents/TempWorkingFolder_Deletable/Aim3/Output_04302019/Aim3_RawRegressionResult_Coef_10302019.txt", header=TRUE, as.is=TRUE)
str(test)


# PheWASplot_EA3_10302019 800*500
ggplot(test, aes(x=Variable, y=log(P_EA3))) + scale_y_continuous(breaks = seq(0, 500, 10)) + ylim(c(-0.1, -375)) + geom_point(aes(col=Category_A), size=3) + theme_classic() + geom_text_repel(data=. %>% mutate(label = ifelse(P_EA3 < 0.000000000000000000005, as.character(Variable), "")), aes(label=label), size=3.9, box.padding = 0.3) + theme(axis.text.x = element_blank(), panel.grid.minor=element_line(colour = "grey", linetype="dashed"), axis.ticks=element_blank()) + geom_hline(yintercept=log(0.00086206), color="red", size=1, alpha=0.5) + labs(color="Category", size="Effect size", x="Phenotypes", y="log(p-value)", title="(a) PheWAS plot of Educational Attainment(EA) GPS") 
ggplot(test, aes(x=Variable, y=log(P_CP))) +  scale_y_continuous(breaks = seq(0, 500, 10)) + ylim(c(-0.1, -452)) + geom_point(aes(col=Category_A), size=3) + theme_classic() + geom_text_repel(data=. %>% mutate(label = ifelse(P_CP < 0.0000000000000000001, as.character(Variable), "")), aes(label=label), size=3.9, box.padding = 0.3) + theme(axis.text.x = element_blank(), axis.ticks=element_blank(), panel.grid.minor=element_line(colour = "grey", linetype="dashed")) + geom_hline(yintercept=log(0.00086206), color="red", size=1, alpha=0.5) + labs(color="Category", size="Effect size", x="Phenotypes", y="log(p-value)", title="(b) PheWAS plot of Cognitive Performance (CP) GPS")
ggplot(test, aes(x=Variable, y=log(P_HM))) +  scale_y_continuous(breaks = seq(0, 500, 10)) + ylim(c(0, -360)) + geom_point(aes(col=Category_A), size=3) + theme_classic() + geom_text_repel(data=. %>% mutate(label = ifelse(P_HM < 0.00000000000001, as.character(Variable), "")), aes(label=label), size=3.9, box.padding = 0.3) + theme(axis.text.x = element_blank(), axis.ticks=element_blank(), panel.grid.minor=element_line(colour = "grey", linetype="dashed")) + geom_hline(yintercept=log(0.00086206), color="red", size=1, alpha=0.5) + labs(color="Category", size="Effect size", x="Phenotypes", y="log(p-value)", title="(c) PheWAS plot of GPS Highest Math (HM) GPS") 
ggplot(test, aes(x=Variable, y=log(P_MA))) +  scale_y_continuous(breaks = seq(0, 500, 10)) + ylim(c(0, -270)) + geom_point(aes(col=Category_A), size=3) + theme_classic() + geom_text_repel(data=. %>% mutate(label = ifelse(P_MA < 0.000000005, as.character(Variable), "")), aes(label=label), size=3.9, box.padding = 0.3) + theme(axis.text.x = element_blank(), axis.ticks=element_blank(), panel.grid.minor=element_line(colour = "grey", linetype="dashed")) + geom_hline(yintercept=log(0.00086206), color="red", size=1, alpha=0.5) + labs(color="Category", size="Effect size", x="Phenotypes", y="log(p-value)", title="(d) PheWAS plot of GPS Math Ability (MA) GPS") 
 


