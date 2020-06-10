# A critical analysis of the IGC gene catalog
The Integrated Gene Catalog (IGC) is a set of ~9.8 million reference genes from the human gut microbiome. Here, we provide the data and code used for our analysis. Our analysis focused on both the approach used to construct this catalog and its effectiveness when used as a reference for microbiome studies. Our results highlight important limitations of the approach used to construct the IGC and call into question the broad usefulness of gene catalogs more generally.

## Download IGC data 
We downloaded the [data](http://gigadb.org/dataset/100064) provided by the authors of the IGC including: the catalogs for the IGC, AGC, CGC, EGC, and SPGC; information about the metagenomic samples used to construct those catalogs; the predicted ORF's; the taxonomic and functional annotations for the clusters; and the gene clustering output files which were used to identify the cluster members of all IGC representatives. The data files specific to our analysis can be found [here](https://obj.umiacs.umd.edu/igc-analysis/IGC_analysis_data.tar.gz).

## Associating gene sequences from all samples to the IGC cluster representative
The IGC provides the representative sequences from gene clustering as a reference database. For our analysis, however, we needed all the cluster members that clustered to their representative sequences. These relationships can be determined from the CD-Hit clustering output files (i.e. AGC.clstr, EGC.clst, CGC.clstr, SPGC.clstr, 3CGC.clstr and IGC.clstr). We provide the file IGCcluster_of_clusters.txt which contains each IGC cluster representative (first gene per line) and its cluster members (all genes following the first per line).

## Increase in cluster diameter due to multiple rounds of clustering - *Transitive Clustering Error* 
In construction of a catalog, genes from metagenome samples are clustered together based on similarity in order to remove redundancy due to fragmentary data, sequencing errors, or small strain-level variants. IGC was constructed with multiple sequential rounds of clustering to handle the scale of such data. However, the multi-round process yields clusters with a (much) wider diameter. We call this methodological error *transitive clustering error* which occurs when different gene catalogs are sequentially clustered.

To detect transitive clustering error in the IGC, 255,191 IGC gene clusters with at least 100 sequences were analyzed. Each gene cluster with all its members were clustered with CD-HIT using two different sets of parameters: 1) The IGC parameters, ≥95% identity and ≥90% query coverage (-c 0.95 -aS 0.9 -g 1 -G 0); 2) relaxed parameters, ≥50% identity and ≥90% query coverage (-n 3 -c 0.50 -aS 0.9 -g 1 -G 0). For parameter set 1, the number of resulting clusters was simply counted and compared to the original number of clusters. For parameter set 2, we parsed the CD-HIT output files with measure_TCE_IGC_clusters_50pident.py to identify the cluster member with the minimum percent identity to the representative. If the cluster was split into two or more partitions the minimum percent identity was recorded as “< 50%”.
```
python measure_TCE_IGC_clusters_50pident.py cdhit_gene_cluster_file.clstr
```
## Gene length variance 
IGC does not require full-length alignments to each cluster representative, rather it allows matches that cover as little as 90% of the clustered sequence. For IGC gene clusters with at least 100 sequences, we calculated maximum length difference between sequences assigned to same cluster. 

## Taxonomic inhomogeneity
The 95% identity cutoff selected by the IGC was intended to create clusters with taxonomic homogeneity at the species level. 
To evaluate the taxonomic homogeneity within the actual IGC clusters, we aligned each sequence within a cluster to the NCBI nr database using Diamond (--query-cover 90 --id 95). We sampled 236 IGC clusters (the 104 largest clusters and 132 randomly chosen clusters with at least 100 sequences each). We inferred the number of species per gene cluster with two approaches: 1) Counting the number of species per cluster only using the top hit for each sequence; 2) identifying the smallest number of species such that each sequence had at least one significant Diamond hit to one of these species i.e. calculating the minimum set cover. Because calculating the minimum set cover is a NP-hard problem, we approximated the minimum set cover with a greedy approach. The input for this program is the Diamond output in format 6.
```
python coverset.py diamond_file.txt
```
The output has to be manually curated to get rid of redundandancy. Typical redundancies include multiple strains of the same species or variants of species names.

We also found that sequences from individual species may be broken up across multiple clusters. We analyzed 214,599 Salmonella enterica genomes obtained from the GenomeTrakr database. Within the 1,152 core genes (genes found in all of the analyzed strains) the average sequence identity between homologous genes was just 86.2% which is much lower than the 95% cutoff used by the IGC. In fact, only 25 core genes exceeded the 95% threshold and would have been clustered properly by the IGC. 

## Simulated data and mapping to IGC and SPGC
We simulated three datasets from [507 genomes](https://github.com/SethCommichaux/IGC/blob/master/data/genomes_from_SPGC.txt/) used in costruction of the SPGC using [ART sequence simulator](https://doi.org/10.1093/bioinformatics/btr708). Two samples were simulated as single-end Illumina reads of 100nt and 250 nt, respectively. We simulated 1 sample with 454 sequencing profile. 
```bash
art_illumina -ss HS20 -l 100 -f 5 -i SPGC_genomes.fa -o Illumina_100_reads
art_illumina -ss MSv3  -l 250 -f 5 -i SPGC_genomes.fa -o Illumina_250_reads 
art_454 -M -s -a -d -r 32 SPGC_genomes.fa  454_reads 5
```
We aligned reads from these dataset to the IGC using BLAST, BOWTIE2, and BWA-MEM. 
```bash
bowtie2 -x IGC_index reads.fq -p 8 | samtools view -bS - > reads.bam
blastn -query reads.fa -db IGC_index -out reads_blast.out  -perc_identity 95 -outfmt " 6 qaccver saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen " 
bwa mem -a -t 12 IGC_index.fa reads.fa  > reads.sam
```
We also aligned Illumina (100nt) dataset to the SPGC using bowtie2 for the Visibility of Species analysis in the paper. 
```bash
bowtie2-align-l --no-unal --no-head -x SPGC_index  -U reads.fa -S map2Spgc.sam --threads 8
```
## Visibility of Species in the SPGC
The SPGC was one of the precursor gene catalogs used to create the IGC. It is composed of the reference genes from 511 reference genomes from species known to occur in the human gut. The fate of sequences (i.e. whether they become representative sequences or cluster members) after gene clustering can be determined from the CD-HIT output file SPGC.clstr. Each identifier is prefixed by the NCBI taxonomic ID of the reference genome. We aggregated these results into tables at the species level (SPGC_hidden_genes.summary, SPGC_hidden_genes.summary.matrix), providing the pairwise statistics for the genes of species that effectively render the genes of other species invisible in the gene catalog.

## Read mapping statistics and gene abundance profiles
For all three simulated datasets, we computed read mapping statistics for the three mapping tools - BLAST, BOWTIE2, and BWA-MEM.
- Number of reads mapping
- Number of reads uniquely mapping
- Number of reads unmapped
- Number of reads multimapped

For BLAST, we only considered alignments that covered 90% of the query sequence and had >=95% percent identity. 
We computed the number of reads aligned to each IGC representative gene. The multi-mapped reads were randomly assigned to one of the mapped IGC genes. The gene abundance profile was created for each combination of readset and mapping tool, normalizing by the number of aligned reads. We use a Mann Whitney U test from Scipy package in Python to compare the gene abundance profiles generated by different mapping tools when mapping simulated reads to the IGC.

## Evaluating the IGC as a reference for a real metagenomic dataset - Cameroon sample analysis
To investigate how read mapping artefacts and species not represented in the catalog impact analyses based on the IGC, we downloaded a human gut sample from a 61-year-old Cameroonian man with a hunter-gatherer diet from NCBI (SRA accession ERR2619707) using SRA Toolkit.
```
fastq-dump --split-3 ERR2619707
```
We modified the read identifiers so the forward and reverse reads were identifiable in the Bowtie2 output (e.g. read ERR2619707.3 from the forward reads fastq file was modified to ERR2619707.1.3). The reads were assembled with MegaHit and genes were predicted using Prokka using default settings for both. The predicted genes that could be assigned to IGC clusters (i.e. had a best BLASTN hit over ≥95% identity and ≥90% query coverage to an IGC cluster) became the Clustered Predicted Genes. The predicted genes that couldn't be assigned to an IGC cluster became the Unclustered Predicted Genes. Reads were then mapped with Bowtie2 to the IGC and the predicted genes under two different conditions.

1) Not requiring concordant mapping
```
bowtie2 -x predicted_genes_index -U ERR2619707.fastq -S ERR2619707.all_genes.sam
bowtie2 -x IGC_genes_index -U ERR2619707.fastq -S ERR2619707.igc.sam
```
2) Requiring concordant mapping
```
bowtie2 --no-mixed --no-discordant -x predicted_genes_index -1 ERR2619707_1.fastq -2 ERR2619707_2.fastq -S ERR2619707.all_genes.concordant.sam
bowtie2 --no-mixed --no-discordant -x IGC_genes_index -1 ERR2619707_1.fastq -2 ERR2619707_2.fastq -S ERR2619707.igc.concordant.sam
```
Read mapping statistics were then gathered and output with analyze_cameroon.py
```
python analyze_cameroon.py -fastq ERR2619707.fastq -genes predicted_genes.fasta -clustered clustered2IGC.blast -sam_pred_genes_nc ERR2619707.all_genes.sam -sam_pred_genes_cord ERR2619707.all_genes.concordant.sam -sam_igc_nc ERR2619707.igc.sam -sam_igc_cord ERR2619707.igc.concordant.sam

```
The data files necessary to run this command can be downloaded using the link in the Download IGC data section.
