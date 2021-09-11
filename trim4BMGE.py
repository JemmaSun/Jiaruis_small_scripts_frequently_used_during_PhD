#!/usr/bin/env python

import argparse

markers=['PF00368.13', 'PF00410.14', 'PF00466.15', 'PF00687.16', 'PF00827.12', 'PF00900.15', 'PF01000.21', 'PF01015.13', 'PF01090.14', 'PF01092.14', 'PF01157.13', 'PF01191.14', 'PF01194.12', 'PF01198.14', 'PF01200.13', 'PF01269.12', 'PF01280.15', 'PF01282.14', 'PF01496.14', 'PF01655.13', 'PF01798.13', 'PF01864.12', 'PF01866.12', 'PF01868.11', 'PF01984.15', 'PF01990.12', 'PF02006.11', 'PF02978.14', 'PF03874.11', 'PF04019.7', 'PF04104.9', 'PF04919.7', 'PF07541.7', 'PF13656.1', 'PF13685.1', 'TIGR00021', 'TIGR00037', 'TIGR00042', 'TIGR00064', 'TIGR00111', 'TIGR00134', 'TIGR00240', 'TIGR00264', 'TIGR00270', 'TIGR00279', 'TIGR00283', 'TIGR00291', 'TIGR00293', 'TIGR00307', 'TIGR00308', 'TIGR00323', 'TIGR00324', 'TIGR00335', 'TIGR00336', 'TIGR00337', 'TIGR00373', 'TIGR00389', 'TIGR00392', 'TIGR00398', 'TIGR00405', 'TIGR00408', 'TIGR00422', 'TIGR00425', 'TIGR00432', 'TIGR00442', 'TIGR00448', 'TIGR00456', 'TIGR00458', 'TIGR00463', 'TIGR00468', 'TIGR00471', 'TIGR00490', 'TIGR00491', 'TIGR00501', 'TIGR00521', 'TIGR00522', 'TIGR00549', 'TIGR00658', 'TIGR00670', 'TIGR00729', 'TIGR00936', 'TIGR00982', 'TIGR01008', 'TIGR01012', 'TIGR01018', 'TIGR01020', 'TIGR01025', 'TIGR01028', 'TIGR01038', 'TIGR01046', 'TIGR01052', 'TIGR01060', 'TIGR01077', 'TIGR01080', 'TIGR01213', 'TIGR01309', 'TIGR01952', 'TIGR02076', 'TIGR02153', 'TIGR02236', 'TIGR02258', 'TIGR02338', 'TIGR02389', 'TIGR02390', 'TIGR02651', 'TIGR03626', 'TIGR03627', 'TIGR03628', 'TIGR03629', 'TIGR03636', 'TIGR03653', 'TIGR03665', 'TIGR03670', 'TIGR03671', 'TIGR03672', 'TIGR03673', 'TIGR03674', 'TIGR03677', 'TIGR03680', 'TIGR03683','TIGR03684','TIGR03722']

def trimFile(inputfile,outputfile):
    "Remove any genomes from the MSAs which are just gaps. And return IDs of these removed genomes."
#    hmm= inputfile.split('/')[-1][5:-4]
#    g=open("trimmed_"+hmm+".faa",'w')
    g=open(outputfile,'w')
    with open(inputfile) as infile:
        f=infile.readlines()
    removed=[]
    seq = ''
    for line in f:
        if line.startswith(">"):
            if seq != '':
                if len(seq) > seq.count("-"):
                    g.write(acc)
                    g.write(line)
                else:
                    removed.append(acc.strip()[1:])
            acc = line
            seq = ''
        else:
            seq+=line.strip()
    g.close()
    #print(inputfile+":"+','.join(removed))
    print(len(removed))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='To remove any genomes from the MSA which are just gaps')
    parser.add_argument('-i','--input_MSA', help="Input single MSA file name.",required=True)
    parser.add_argument('-o','--output_MSA', help="Output single MSA file name.",required=True)
    args = parser.parse_args()
    trimFile(args.input_MSA,args.output_MSA)
    print('Done.')
