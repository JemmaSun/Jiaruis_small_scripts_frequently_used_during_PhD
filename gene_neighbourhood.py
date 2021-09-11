#!/usr/bin/python

import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="Prepare input file for Gene Graphics tool (https://katlabs.cc/genegraphics/).\n\nInput file is a text file made up of gff file lines (except header lines) of your targeted genes, where this script can grep gene/genome IDs, positions, annotations from. And yes you can concatenate gff lines from multiple genomes. \n\nOutput file is a tab-separated file named 4GeneGraphicsTool.tsv",formatter_class=RawTextHelpFormatter)
parser.add_argument('-i','--input_gff', help='Text file contains lines from .gff file.',required=True)

input_gff = parser.parse_args().input_gff

# Gene_Graphics_tool = 'https://katlabs.cc/genegraphics/'



g = open('4GeneGraphicsTool.tsv','w')
g.write('\t'.join('Genome ID  Start   Stop    Size (nt)   Strand  Function    Gene Name   Color'.split())+'\n')
with open(input_gff) as f:
    for line in f:
        l=line.strip().split('\t')
        ID = l[8].split('ID=')[-1].split(';')[0]
        gn,start,end,strand = l[0],l[3],l[4],l[6]
        size = str(int(end)-int(start)+1)
        if 'product=' in line:
            function = line.strip().split('product=')[-1].split(';')[0]
        else:
            function = 'n.a.'
        if function == 'hypothetical protein':
            gene = 'hp' 
        elif 'gene=' in line:
            gene = line.strip().split('gene=')[-1].split(';')[0]
        elif 'Name=' in line:
            gene = line.strip().split('Name=')[-1].split(';')[0]
        elif 'eC_number=' in line:
            gene = 'EC'+line.strip().split('eC_number=')[-1].split(';')[0]
        else:
            gene = ID
        g.write('\t'.join([gn,ID,start,end,size,strand,function,gene])+'\t#C4C608\n')
