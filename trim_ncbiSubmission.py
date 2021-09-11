#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Trim adapters reported by NCBI WGS genome submission portal.')
parser.add_argument('-i','--genome_file', help="genome file to be trimmed.",required=True)
parser.add_argument("-c","--triming_file", help="NCBI contamination report. Only keep lines which contain Regions need to be trimmed start after line 'Trim:' followed a header line. e.g. k141_100662  6845    6767..6845  adaptor:multiple",required=True)
args = parser.parse_args()

genome_file = args.genome_file #'A_ERP013176_bin.4_Janus.fa'
# MAG file
triming_file = args.triming_file #'Contamination_ERP013176_bin_4.txt'
# NCBI contamination report. Only keep lines which contain Regions need to be trimmed start after line "Trim:" followed a header line

def trim_genome(genome_file, triming_region):
    """
    triming_region: dictionary => {contig_ID:[start,end]}
    """
    with open(genome_file) as f:
        g = open('trimmed_'+ genome_file,'w')
        contig = ''
        for line in f:
            if line.startswith('>'):
                if contig != '':
                    if contig in triming_region.keys():
                        tr = triming_region[contig]
                        i = 0
                        new_seq = ''
                        while i < len(tr):
                            new_seq += seq[tr[i]:tr[i+1]]
                            i+=2
                        seq = new_seq
                    g.write('>'+contig+'\n'+seq+'\n')
                contig = line.strip().split()[0][1:]
                seq = ''
            else:
                seq += line.strip()
    g.close()

if __name__ == "__main__":
    triming_region = {}
    with open(triming_file) as f:
        for line in f:
            l = line.strip().split()
            contig = l[0]
            triming_region[contig] = [0]
            regions = l[2].split(',')
            for region in regions:
                s,e = int(region.split('..')[0])-1, int(region.split('..')[1])-1
                triming_region[contig]+=[s,e]
            triming_region[contig].append(int(l[1]))
    trim_genome(genome_file, triming_region) 
