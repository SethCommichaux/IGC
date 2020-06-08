import argparse

def main():
    parser = argparse.ArgumentParser(description="Groups the sequences based on their lineage")
    parser.add_argument("-m","--metadata", help="SPGC metadata file",required = True)
    parser.add_argument("-t","--taxon_file", help="SPGC taxon ID file",required = True)
    # parser.add_argument("-pid ","--pid", help="Percent identity threshold (Not required) ",required=False, default = 0)
    # parser.add_argument("-qcov","--query_cov", help="Query coverage (between 0 and 1)",required=False, default = 0.90)
    parser.add_argument("-out","--op_file", help="Output file prefix",required=True)
    args = parser.parse_args()

    #Read the SPGC taxon file
    taxon_map = {}
    with open(args.taxon_file) as f:
        for line in f:
            taxon_map[line.strip()] = 1

    #Get the taxon to species map
    taxon2species = {}
    taxon_heirarchy = {}
    with open(args.metadata) as f:
        for line in f:
            val = line.strip().split('\t')
            if val[0] not in taxon_map:
                continue
            taxa = val[13].split('|')
            taxa_rank =  val[14].split('|')
            # print taxa, taxa_rank
            if "species" in taxa_rank:  
                species_index = taxa_rank.index('species')
                taxon2species[val[0]] = taxa[species_index]