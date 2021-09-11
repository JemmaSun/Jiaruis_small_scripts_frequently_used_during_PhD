#!/usr/bin/env python

import argparse


ranks = {'phylum':2,'class':3,'order':4,'family':5,'genus':6}

def get_leaf_ids(treefile):
    """
    Generate a list of lead ids following the order of the final tree.
    Input: rooted tree file (not decorated)
    """
    f = open(treefile)
#    tree = f.readline()
    tree = ''.join(f.read().split('\n'))
    f.close()
    l = tree.strip().split(',')
    leaves = []
    for i in l:
        name = ''
        for letter in i:
            if letter == ':':
                break
            elif letter not in ["(",")","'"]:
                name += letter
        if not name.startswith('RS'):
            if not name.startswith('GB'):
                if not name.startswith('U_'):
#                    raise ValueError('Un-recognised gtdb ID: {}, go check!'.format(name))
                    print('Un-recognised gtdb ID: {}.'.format(name))
        leaves.append(name)
    return leaves


def make_group(treefile,alnfile,nds_file,rank): #(treefile,nds_file,rank):
    """
    Apply taxonomy (only to the given rank level, e.g. phylum level) to each in the leaves list obtained from above function.
    """
    if treefile:
        leaves = get_leaf_ids(treefile)
    else:
        f = open(alnfile)
        leaves = []
        for l in f:
            if l.startswith('>'):
                leaves.append(l.strip().split('\t')[0][1:])
        f.close()
    print('Num of ids:'+str(len(leaves))+', is the number correct?')
    f = open(nds_file)
    taxas = {}
    for line in f:
        l = line.strip().split('\t')
        name = l[0]
        try:
            taxa = (';'.join(l[1].split('/'))).split(';')
        except IndexError:
            print(l)
        if len(taxa) >= ranks[rank]:
            taxas[name] = ';'.join(taxa[0:ranks[rank]])
        else:
            taxas[name] = ';'.join(taxa)
    nds = {}    # nds = {taxa1:[startID,endID]}
    for i in leaves: #range(len(leaves)):
        taxa = taxas[i]
        if taxa in nds:
            nds[taxa][1] = i
        else:
            nds[taxa] = [i,'null']
    return nds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate collapse file and label file for iTOL from gtdb rooted tree, or any un-decorated tree file with gtdb name as node ID.')
    parser.add_argument('-ft','--tree_file', help='Must be an undecorated tree, e.g. gtdb_rooted.tree',required=False)
    parser.add_argument('-fa','--aln_file', help='The original alignment file generated with your tree, e.g. gtdb_concatenated.faa',required=False)
    parser.add_argument('-fn','--nds_file', help='Exported TAB-separated NDS file from gtdb ARB, only need two field: name + taxonomy(10).', required=True)
    parser.add_argument('-r','--rank', help='The taxonomy rank that you want to collapse, select from phylum, class, order, family, genus.',required=True)
#    parser.add_argument("--rel", default=False, action="store_true" , help="...")
    args = parser.parse_args()
    treefile = args.tree_file
    nds_file = args.nds_file
    alnfile = args.aln_file
    rank = args.rank

    nds = make_group(treefile,alnfile,nds_file,rank)

    g1 = open('4itol_collapse.txt','w')
    g1.write('COLLAPSE\nDATA\n')
    g2 = open('4itol_labels.txt','w')
    g2.write('LABELS\nSEPARATOR COMMA\nDATA\n')
    for taxa,ids in nds.items():
        if not ids[1]=='null':
            if len(taxa.split(';'))>1:
                g1.write(ids[0]+'|'+ids[1]+'\n')
                g2.write(ids[0]+'|'+ids[1]+','+taxa.split(';')[-1]+'\n')
    g1.close()
    g2.close()
    print('done!')
