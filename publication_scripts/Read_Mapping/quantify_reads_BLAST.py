import argparse
import random
def main():
    parser = argparse.ArgumentParser(description="Calculates the number of reads that were uniquely mapped vs. multimapped ")
    parser.add_argument("-b","--blast_op", help="BLAST ouput file path",required = True)
    parser.add_argument("-pid ","--pid", help="Percent identity threshold ",required=False, default = 95)
    parser.add_argument("-qcov","--query_cov", help="Query coverage (between 0 and 1)",required=False, default = 0.90)
    parser.add_argument("-o","--output_file", help="Gene counts output file",required=False, default = "gene_counts.txt")
    args = parser.parse_args()

    # Read the BLAST output file
    reads_selected = {}
    multimapped_reads = {}
    unique = 0
    multimapped = 0
    multimapped_genes =  {}
    none = 0
    gene = {}
    total = {}
    with open(args.blast_op) as f:
        for line in f:
            val = line.strip().split('\t')
            total[val[0]] = 1
            qc = (abs(int(val[7]) - int(val[6])) + 1)/ int(val[-1])
            pid = float(val[2]) 
            bitscore = float(val[-2])

            if qc >= float(args.query_cov) and pid >= float(args.pid):
                value2store = (qc, pid, bitscore, val[1])
                if val[0] in reads_selected:
                    #Reads are considered multi-mapped if they have same bitscore and qualify pid and qc thresholds
                    if bitscore == reads_selected[val[0]][2]:
                        multimapped_reads[val[0]] = 1
                        if val[0] in multimapped_genes:
                            multimapped_genes[val[0]].append(val[1])
                        else:
                            multimapped_genes[val[0]] = []
                            multimapped_genes[val[0]].append(reads_selected[val[0]][3])
                            multimapped_genes[val[0]].append(val[1])

                    if bitscore > reads_selected[val[0]][2]:
                        reads_selected[val[0]] = value2store
                        gene[val[0]] = val[1]
                        
                else:
                    reads_selected[val[0]] = value2store
                    gene[val[0]] = val[1]
    gene_counts = {}
    for key in reads_selected:
        none += 1
        if key in multimapped_reads:
            multimapped += 1
            gene_name = random.choice(multimapped_genes[key])
        else:
            unique += 1
            gene_name = gene[key]
        if gene_name in gene_counts:
            gene_counts[gene_name] += 1
        else:
            gene_counts[gene_name] = 1

    fw = open(args.output_file, 'w')
    print ("#For %f percent identity and %f query coverage, %d aligned 0 times, %d aligned exactly once, and %d aligned more than once" %(float(args.pid), float(args.query_cov), len(total)-none, unique, multimapped ))
    fw.write("#For %f percent identity and %f query coverage, %d aligned 0 times, %d aligned exactly once, and %d aligned more than once" %(float(args.pid), float(args.query_cov), len(total)-none, unique, multimapped ))
    for key in gene_counts:
        fw.write(key + '\t' + str(gene_counts[key])+'\n')

if __name__ == '__main__':
    main()
