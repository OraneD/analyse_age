
#install.packages("sciplot") 
#install.packages("languageR") 

library(sciplot)
library(languageR)




rm (list=ls(all=TRUE))


setwd("/media/orane/MAXTOR/Memoire/")


file1 = "resultats_corpus_mfa_avec_md_utf8.xls"
donnees = read.table(file1, header = TRUE, na.strings = "--undefined--", 
                      strip.white=TRUE, stringsAsFactors = FALSE, sep="\t",
                      dec = ".", encoding = "UTF-8", fill=TRUE)


View(donnees)

donnees_voyelles = donnees[(donnees$phoneme=="a" | donnees$phoneme=="i" | 
donnees$phoneme=="y" | donnees$phoneme=="ɔ" | donnees$phoneme=="u" | 
  donnees$phoneme=="ɑ̃" | donnees$phoneme=="ɛ" | donnees$phoneme=="o"
| donnees$phoneme=="ɑ"| donnees$phoneme=="ɔ̃" | donnees$phoneme=="ɛ"
| donnees$phoneme=="ɛ̃"| donnees$phoneme== "œ"
),]

donnees_voyelles = donnees[(donnees$phoneme=="f" | donnees$phoneme=="s" | 
                              donnees$phoneme=="ʃ" | donnees$phoneme=="v" | donnees$phoneme=="z" | 
                              donnees$phoneme=="ʒ" | donnees$phoneme=="ʁ"),]

donnees_voyelles = donnees[(donnees$phoneme=="_"),]
donnees_voyelles = donnees[(donnees$phoneme=="s"),]

bargraph.CI(age, data = donnees_voyelles, duree,
            xlab = "age", ylab = "duree_pauses", cex.lab = 1, ylim = c(0,260), 
            x.leg = 1, y.leg = 0.36, bty="y",cex.names = 1,las=2, err.width=0.02,fun = function(x) mean(x, na.rm=TRUE),
            ci.fun= function(x) c(mean(x, na.rm=TRUE), mean(x, na.rm=TRUE)+se(x)),
            density = c(0,20), legend = TRUE)

View(donnees_voyelles)

