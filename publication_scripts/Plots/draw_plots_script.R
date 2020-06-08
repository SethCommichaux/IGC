library(ggplot2)
library(cowplot)
require(scales)

pdf("icl_final.pdf")
ggplot(data = icl, aes(x=V1))+
  geom_histogram() + scale_x_log10(labels = comma)+ scale_y_continuous(labels= comma) +
  labs(
    x = "Maximum intra-cluster gene length difference", 
    y = "Number of IGC clusters") + theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black')) + theme(axis.line = element_line(colour = "black"))
dev.off()
icl <- read.csv('intracluster_length_distribution.txt',sep = '\t', header = FALSE)
v <- ggplot(data = icl, aes(x=V1))+
  geom_histogram() + scale_x_log10(labels = comma)+ scale_y_continuous(labels= comma) +
  labs(
    x = "Maximum intra-cluster gene length difference", 
    y = "Number of IGC clusters") + theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))
v

tceset <- read.csv('TCE_most_diverent_cdhit_updatedremovedlt60.txt',sep = ' ', header=FALSE)
w <- ggplot(data = tceset, aes(x=V2)) + 
  geom_histogram() +  geom_vline(xintercept = 95, linetype="solid", color = "red")+
  labs(x = "Percent Identity between the representative sequence\n and the most divergent cluster member", y = "Number of IGC clusters") + theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))
w
pdf("maxintracluster_pid.pdf")
ggplot(data = tceset, aes(x=V2)) + 
  geom_histogram() +  geom_vline(xintercept = 95, linetype="solid", color = "red")+
  labs(x = "Percent Identity between the representative sequence\n and the most divergent cluster member", y = "Number of IGC clusters") + theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))  + theme(axis.line = element_line(colour = "black"))
dev.off()

### Core genes SE
a <- read.csv('core_gene_analysis_salmonella_all_core_genes.txt', sep='\t', header = FALSE)
pnew <- ggplot(data=a, aes(x=V1)) + 
  geom_histogram() +
  geom_vline(aes(xintercept=95), color="red", linetype="solid") +
  labs(x="Minimum sequence identity between homologous core genes", y = "Number of genes (clusters)") + theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))  + theme(axis.line = element_line(colour = "black"))

setvals <- read.csv('IGC_taxonomic_composition_counts.csv', sep = ',', header=TRUE)
s <- ggplot(data=setvals, aes(x=Minimum_Set_Cover)) + 
  geom_histogram() + 
  labs(x = "Minimum number of species to \"cover\" sequences in a gene cluster", 
       y = "Number of gene clusters")+ theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))  + theme(axis.line = element_line(colour = "black"))
s
t <- ggplot(data = setvals, aes(x=Diamond_Best_Hit))+
  geom_histogram() + 
  labs(
    x = "Number of species using Diamond top-hit per gene cluster", 
    y = "Number of gene clusters")+ theme_light() + theme(axis.text.x = element_text(size=12,color='black'), axis.text.y = element_text(size=12,color='black'), axis.title.x = element_text(size=12,color='black'), axis.title.y = element_text(size=12,color='black'))  + theme(axis.line = element_line(colour = "black"))
t

pdf("fig2_final.pdf")
plot_grid(s,t,pnew, labels = c('A', 'B', 'C'), label_size = 14, nrow=1, rel_widths = c(1,1,1))
dev.off()

