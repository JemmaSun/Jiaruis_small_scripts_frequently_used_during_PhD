#!/usr/bin/env python

import argparse

def countGC(seq):
    cnt = 0
    for i in seq:
        if i == 'G' or i=='C' or i=='g' or i=='c':
            cnt += 1
    return 100*float(cnt)/float(len(seq))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count GC content')
    parser.add_argument('-i','--genome', help='Name of your genomes file.',required=True)
    args = parser.parse_args()
    genome = args.genome
    #g = open('gc_counts.tsv','w')
    with open(genome) as f:
        seq = ''
        for line in f:
            if not line.startswith('>'):
                seq += line.strip()
        if seq != '':
            gc = countGC(seq)
    print('Average GC of {0} is:{1}%'.format(genome,str(gc)))        
