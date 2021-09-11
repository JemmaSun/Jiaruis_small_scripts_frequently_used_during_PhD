#!/usr/bin/env python

import argparse

def filter(samples):
    for sample in samples:
        cnt=0
        with open(sample+'/'+sample+'.hmmout.txt') as f:
            for line in f:
                if not line.startswith('#'):
                    hit = line.strip().split()
                    evalue,score = float(hit[11]),float(hit[13])
                    if (evalue <= e_max) and (score >= s_min):
                        cnt +=1
        print(sample+'\t'+str(cnt))

def filter_with_seq(samples):
    hits=''
    g=open('filtered_sequences.fa','w')
    for sample in samples:
        cnt=0
        passed_acc=[]   # protein accession that pass filtering.
        with open(sample+'/'+sample+'.hmmout.txt') as f:
            for line in f:
                if not line.startswith('#'):
                    hit = line.strip().split()
                    acc = hit[0]
                    evalue,score = float(hit[11]),float(hit[13])
                    if (evalue <= e_max) and (score >= s_min):
                        cnt +=1
                        passed_acc.append(acc)
        hits+=(sample+'\t'+str(cnt)+'\n')
        fa_file=sample+'/'+sample+'_hits.fa'
        g.write(get_seq(passed_acc,fa_file))
    print(hits)
    g.close()
    

def get_seq(accs,fa_file):   # Copy from ~/my_py/get_seq_from_fa.py
    sequences=''
    with open(fa_file) as f:
        seq=''
        for line in f:
            if line.startswith('>'):
                if seq != '':
                    sequences += seq+'\n'
                seq=''
                record=False
                header=line.strip().split()[0][1:]
                if header in accs:
                    record=True
                    seq='>'+header+'\t'+fa_file.split('/')[-1]+'\n'
            else:
                if record:
                    seq+= line.strip()
        if seq != '':
            sequences +=seq+'\n'
    return sequences

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Further filtering GraftM hits; Run this @ /GraftM_output/')
    parser.add_argument('-e','--evalue', help='e-value threshold value',default='1',required=False)
    parser.add_argument('-s','--score', help='Score threshold value.',default='0',required=False)
    parser.add_argument('-so','--seqout', help='Print protein sequences that pass the criteria. Default not print.',default=False, action="store_true")
    args = parser.parse_args()

    e_max = float(args.evalue)
    s_min = float(args.score)

    with open('search_otu_table.txt') as f:
        samples=[l for l in f.readline().strip().split()[1:]]

    if args.seqout:
        filter_with_seq(samples)
        print('Sequences written to filtered_sequences.fa.')
    else:
        filter(samples)
    print('Done.')
