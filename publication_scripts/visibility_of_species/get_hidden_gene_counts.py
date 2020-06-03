import argparse

def main():
    parser = argparse.ArgumentParser(description="Groups the sequences based on their lineage")
    parser.add_argument("-m","--metadata", help="SPGC metadata file",required = True)
    parser.add_argument("-c","--clstr_file", help="Cd-hit clstr file",required = True)
    # parser.add_argument("-pid ","--pid", help="Percent identity threshold (Not required) ",required=False, default = 0)
    # parser.add_argument("-qcov","--query_cov", help="Query coverage (between 0 and 1)",required=False, default = 0.90)
    parser.add_argument("-out","--op_file", help="Output file prefix",required=True)
    args = parser.parse_args()

    #Get the taxon to species map
    taxon2species = {}
    with open(args.metadata) as f:
        for line in f:
            val = line.strip().split('\t')
            taxa = val[13].split('|')
            taxa_rank =  val[14].split('|')
            # print taxa, taxa_rank
            if "species" in taxa_rank:  
                species_index = taxa_rank.index('species')
                taxon2species[val[0]] = taxa[species_index]
            # print taxon2species
            

    #read the cluster file
    hide_genes = {}
    hide_genes_length = {}
    num_centroid = {}
    num_genes = {}
    num_redundant = {}
    num_lines = 0
    centroid = None
    centroid_len = 0
    taxon_seen = {} 
    with open(args.clstr_file) as f:
        for line in f:
            if line.startswith('>'):
                continue
            lineval = line.strip().split('\t')
            taxon_num = lineval[1].split('>')[1].split('.')[0]
            taxon_seen[taxon_num] = 1
            length = int(lineval[1].split('>')[0].split('nt')[0])   
            if lineval[0] == '0':
                if taxon_num in taxon2species:
                    centroid = taxon2species[taxon_num]
                    centroid_len = length
                else:
                    print "Centroid - No species found", taxon_num
                    centroid = None
                    centroid_len = 0
                if centroid in num_centroid:
                    num_centroid[centroid] += 1
                    num_genes[centroid] += 1
                else:
                    num_centroid[centroid] = 1
                    num_genes[centroid] = 1
            else:
                if taxon_num in taxon2species:
                    redundant = taxon2species[taxon_num]
                    if redundant in num_genes:
                        num_genes[redundant] += 1
                    else:
                        num_genes[redundant] = 1
                    if centroid in hide_genes:
                        if redundant in hide_genes[centroid]:
                            hide_genes[centroid][redundant] += 1
                        else:
                            hide_genes[centroid][redundant] = 1
                    else:
                        hide_genes[centroid] = {}
                        hide_genes[centroid][redundant] = 1
                    if length < centroid_len:
                        if centroid in hide_genes_length:
                            if redundant in hide_genes_length[centroid]:
                                hide_genes_length[centroid][redundant] += 1
                            else:
                                hide_genes_length[centroid][redundant] = 1
                        else:
                            hide_genes_length[centroid] = {}
                            hide_genes_length[centroid][redundant] = 1
                else:
                    print "Redundant - No species found", taxon_num
                # print lineval, "hi", hide_genes, hide_genes_length, num_genes, num_centroid
                # break

    fw = open(args.op_file+'_hidden_genes.summary', 'w')
    fw.write("#Species_that_hide(A)\tSpecies_that's_hidden(B)\thow_often?\tnum_centroids_A\tnum_centroids_B\tnum_genes_A\tnum_genes_B\n")
    for key in hide_genes:
        if key in num_centroid:
            num_centroids_A = str(num_centroid[key])
        else:
            num_centroids_A = '0'
        if key in num_genes:
            num_genes_A = str(num_genes[key])
        else:
            num_genes_A = '0'
        for key2 in hide_genes[key]:
            if key2 in num_centroid:
                num_centroids_B = str(num_centroid[key2])
            else:
                num_centroids_B = '0'
            if key2 in num_genes:
                num_genes_B = str(num_genes[key2])
            else:
                num_genes_B = '0'

            fw.write(key + "\t" + key2 + '\t' + str(hide_genes[key][key2]) + '\t' + num_centroids_A + '\t' + num_centroids_B + '\t' + num_genes_A + '\t' + num_genes_B +'\n')

    fw.close()
            
    fw = open(args.op_file+'_hidden_genes_shorter_length.summary', 'w')
    fw.write("#Species_that_hide(A)\tSpecies_that's_hidden_causeof_shorter_length(B)\thow_often?\tnum_centroids_A\tnum_centroids_B\tnum_genes_A\tnum_genes_B\n")
    for key in hide_genes_length:
        if key in num_centroid:
            num_centroids_A = str(num_centroid[key])
        else:
            num_centroids_A = '0'
        if key in num_genes:
            num_genes_A = str(num_genes[key])
        else:
            num_genes_A = '0'
        for key2 in hide_genes_length[key]:
            if key2 in num_centroid:
                num_centroids_B = str(num_centroid[key2])
            else:
                num_centroids_B = '0'
            if key2 in num_genes:
                num_genes_B = str(num_genes[key2])
            else:
                num_genes_B = '0'

            fw.write(key + "\t" + key2 + '\t' + str(hide_genes_length[key][key2]) + '\t' + num_centroids_A + '\t' + num_centroids_B + '\t' + num_genes_A + '\t' + num_genes_B +'\n')

    fw.close()
    fw = open(args.op_file+'_taxon_ids_in_SPGC.txt', 'w')
    for key in taxon_seen:
        fw.write(str(key)+'\n')
    fw.close()
            

if __name__ == '__main__':
    main()