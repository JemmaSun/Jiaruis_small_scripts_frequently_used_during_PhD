#!/usr/bin/env python

import json
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="Summary and grep the top non-hp blast hits, and output them to stdout.(If the top ten hits are all hypothetical proteins, will output the details for the top one.)\n\nOutput have five columns: Accession, Description, E-value Score, Per.Identity.\n\n As it's unconvenient to directly paste a comma/tab-separated text to Google Sheet, the delimiter used here is =, so please use 'Text to columns' function in excel/google and set the separator to be =.",formatter_class=RawTextHelpFormatter)
parser.add_argument('-i','--jsonfile', help='The Single-file JSON downloaded from blastp website.',required=True)
with open(parser.parse_args().jsonfile) as f:
    d=json.loads(f.read())

for i in range(len(d['BlastOutput2'])):
    try:
        query=d['BlastOutput2'][i]['report']['results']['search']['query_title']
        hits=d['BlastOutput2'][i]['report']['results']['search']['hits']
        desc=hits[0]['description'][0]['title']
        acc=hits[0]['description'][0]['accession']
        e=hits[0]['hsps'][0]['evalue']
        s=hits[0]['hsps'][0]['bit_score']
        identity=100*hits[0]['hsps'][0]['identity']/float(hits[0]['hsps'][0]['align_len'])
    except IndexError:
        print(query+'=no hit found')
        continue
    for j in range(min(len(hits),10)):
        cont=hits[j]
        desc_new=cont['description'][0]['title']
        if 'hypothetical protein' not in desc_new:
            desc=desc_new
            acc=hits[j]['description'][0]['accession']
            e=cont['hsps'][0]['evalue']
            s=cont['hsps'][0]['bit_score']
            identity=100*cont['hsps'][0]['identity']/float(cont['hsps'][0]['align_len'])
            break
    print(query+'='+acc+'='+desc+'='+str(e)+'='+str(s)+'='+str(identity))


