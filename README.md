# A critical analysis of the IGC gene catalog
The Integrated Gene Catalog (IGC) is a set of ~9.8 million reference genes from the human gut microbiome. Here, we provide the data and code used for our analysis. We focus on both the approach used to construct this catalog and its effectiveness when used as a reference for microbiome studies. Our results highlight important limitations of the approach used to construct the IGC and call into question the broad usefulness of gene catalogs more generally.

## Download IGC data 
We downloaded the [data](http://gigadb.org/dataset/100064) provided by the authors of the IGC including: the catalogs for the IGC, AGC, CGC, EGC, and SPGC; information about the metagenomic samples used to construct those catalogs; the predicted ORF's; the taxonomic and functional annotations for the clusters; and the gene clustering output files which were used to identify the cluster members of all IGC representatives.

## Associating gene sequences from all samples to the IGC cluster representative

The IGC provides the representative sequences from gene clustering as a reference database. For our analysis, however, we needed all the cluster members that clustered to their representative sequences. These relationships can be determined from the CD-Hit clustering output files (i.e. AGC.clstr, EGC.clst, CGC.clstr, SPGC.clstr, 3CGC.clstr and IGC.clstr) using the script trace_cluster_generations.py run from a directory where all of the \*clstr files are.

```
python trace_cluster_generations.py
```
This script creates two files: 1) edge_list.txt, which provides all representative-redundant sequence clustering relationships in the IGC; 2) adjacency_list.txt, which provides an adjacency list for cluster membership in the IGC.
### The edge_list and adjacency_list is not clear what they are supposed to mean by their description

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
The output has to be manually curated to get rid of redundandancy -- usually multiple strains of the same species or variants of species names.

We also found that sequences from individual species may be broken up across multiple clusters. We analyzed 214,599 Salmonella enterica genomes obtained from the GenomeTrakr database. Within the 1,152 core genes (genes found in all of the analyzed strains) the average sequence identity between homologous genes was just 86.2% which is much lower than the 95% cutoff used by the IGC. In fact, only 25 core genes exceeded the 95% threshold and would have been clustered properly by the IGC. 

## Simulated data and mapping to IGC and SPGC
We simulated three datasets from [507 genomes](provide_link) used in costruction of the SPGC using [ART sequence simulator](https://doi.org/10.1093/bioinformatics/btr708). Two samples were simulated as single-end Illumina reads of 100nt and 250 nt, respectively. We simulated 1 sample with 454 sequencing profile. 
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
## Visibility of Species in gene catalog

## Read mapping statistics and gene abundance profiles
For all three simulated datasets, we computed read mapping statistics for the three mapping tools - BLAST, BOWTIE2, and BWA-MEM.
- Number of reads mapping
- Number of reads uniquely mapping
- Number of reads unmapped
- Number of reads multimapped

For BLAST, we only considered alignments that covered 90% of the query sequence and had >=95% percent identity. 
We computed number of reads aligning to each IGC representative gene. The reads that were multi-mapped were randomly assigned to one of the IGC gene that it aligned to. The gene abundance profile was created for each dataset and the mapping tool combination, normalizing by the number of aligned reads. We use Mann Whitney U test from Scipy package in Python to compare the gene abundance profiles generated by different mapping tools when mapping simulated reads to the IGC.

## Evaluating IGC as a reference for a real metagenomic dataset - Cameroon sample analysis

