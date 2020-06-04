# Code used for the critical analysis of the IGC
The Integrated Gene Catalog (IGC) is a set of nearly 10 million reference genes from the human gut microbiome.

## Identifying the cluster members of IGC representatives
The IGC provides the representative sequences from gene clustering as a reference database. For our analysis, however, we needed all the cluster members that clustered to their representative sequences. These relationships can be determined from the CD-Hit clustering output files that the IGC author's [provided](http://gigadb.org/dataset/100064) (i.e. AGC.clstr, EGC.clst, CGC.clstr, SPGC.clstr, 3CGC.clstr and IGC.clstr) using the script trace_cluster_generations.py run from a directory where all of the \*clstr files are.

```
python trace_cluster_generations.py
```

This script creates two files: 1) edge_list.txt, which provides all representative-redundant sequence clustering relationships in the IGC; 2) adjacency_list.txt, which provides an adjacency list for cluster membership in the IGC.

## Transitive clustering error analysis

To detect transitive clustering error in the IGC, 255,191 IGC gene clusters with at least 100 sequences were analyzed. Each was clustered with CD-HIT using two different sets of parameters: 1) The IGC parameters, ≥95% identity and ≥90% query coverage (-c 0.95 -aS 0.9 -g 1 -G 0); 2) relaxed parameters, ≥50% identity and ≥90% query coverage (-n 3 -c 0.50 -aS 0.9 -g 1 -G 0). For parameter set 1, the number of resulting clusters was simply counted and compared to the original number of clusters. For parameter set 2, we parsed the CD-HIT output files with measure_TCE_IGC_clusters_50pident.py to identify the cluster member with the minimum percent identity to the representative. If the cluster was split into two or more partitions the minimum percent identity was recorded as “< 50%”.

```
python measure_TCE_IGC_clusters_50pident.py cdhit_gene_cluster_file.clstr
```

## Taxonomic inhomogeneity

To evaluate the taxonomic homogeneity within the actual IGC clusters, we aligned each sequence within a cluster with Diamond to the NCBI nr database (--query-cover 90 --id 95). We sampled 236 IGC clusters (the 104 largest clusters and 132 randomly chosen clusters with at least 100 sequences each). We inferred the number of species per gene cluster with two approaches: 1) Counting the number of species per cluster only using the top hit for each sequence; 2) identifying the smallest number of species such that each sequence had at least one significant Diamond hit to one of these species i.e. calculating the minimum set cover. Because calculating the minimum set cover is a NP-hard problem, we approximated the minimum set cover with a greedy approach using coverset.py. The input for this program is the Diamond output in format 6.

```
python coverset.py diamond_file.py
```




