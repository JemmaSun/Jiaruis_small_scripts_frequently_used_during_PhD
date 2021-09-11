#!/usr/bin/env python

import argparse

def get_seq(accs,fa_file):
#    record=False
    with open(fa_file) as f:
        seq=''
        for line in f:
            if line.startswith('>'):
                if seq != '':
                    #print('>'+header+'\n')
                    print(seq)
                seq=''
                record=False
                header=line.strip().split()[0][1:]
                if header in accs:
                    record=True
#                    seq='>'+header+'\t'+fa_file.split('/')[-1]+'\n'
                    seq='|'.join(line.strip().split('\t'))+'\t'+fa_file.split('/')[-1]+'\n'
            else:
                if record:
                    seq+= line.strip()
        if seq != '':
            print(seq)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Grep select sequences from a fasta file when the sequence are wrote in muliple lines. (2 format of header lines are avaliable, by remove/add # at line 18/19)')
    parser.add_argument('-a','--accessions', help='list of accessions, comma separated')
    parser.add_argument('-i','--listfile', help='File name with accessions')
    parser.add_argument('-f','--fasta', help='Fasta file to grep sequences from.', required=True)
    args = parser.parse_args()
    if args.listfile == None:
        accs = args.accessions.split(',')
    else:
        accs=[]
        with open(args.listfile) as f:
            for line in f:
                accs.append(line.strip())
    fasta= args.fasta
    get_seq(accs,fasta)
