#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""countAssembly.py: gathers stats on assembled FASTA files
"""

__author__ = "Richard Alan White III, Jose Figueroa"
__copyright__ = "Copyright 2021"
__version__ = "0.3"
__maintainer__ = "Jose Figueroa"
__email__ = "jlfiguer@uncc.edu"
__status__ = "Production"

import os
import argparse
import re
import math


# Global variables
FILE_EXT = [".fasta", ".fa", ".fna", ".ffn"]


## main
def main():
    ## Parse the command line
    def typePath(path):
        return (os.path.abspath(os.path.expanduser(path)))

    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--interval", help = "interval size in # of residues", type=int, required = True)
    required.add_argument("-f", "--fasta", help = "fasta file or folder", type=typePath, required = True)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-r", "--ref", help = "reference genome")
    optional.add_argument("-s", "--size", help = "reference genome size")
    optional.add_argument("-h", "--help", action="help", help="show this help message and exit")
    args = parser.parse_args()

    countFasta(args.fasta, args.interval, args.size)

    return 0


def countFasta(assembly, interval, genomeSize):
    files = []
    if os.path.isfile(assembly):
        files = [assembly]
    elif os.path.isdir(assembly):
        files = [os.path.join(assembly, f) for f in os.listdir(assembly) if os.path.splitext(f)[1] in FILE_EXT]
    else:
        print("Not a valid fasta file or directory")
        return

    numSeq = 0
    gcCount = 0
    lengthInter = {}
    seqLengths = []
    for filename in files:
        with open(filename) as fasta:
            id = None
            seqLen = 0
            for line in fasta:
                line = line.strip()
                if line.startswith('>'):
                    # Next sequence in file
                    if id is not None:
                        seqLengths.append(seqLen)
                        inter = math.floor( seqLen/interval )
                        if inter not in lengthInter:
                          lengthInter[inter] = 0
                        lengthInter[inter] += 1
                    # Sequence Basic Info
                    numSeq += 1
                    id = line[1:]
                    seqLen = 0
                elif re.search(r'^[\w]', line) and id is not None:
                    # Sequence data
                    seqLen += len(line)
                    gcCount += len(re.findall('[GC]', line))
            # Incorporate totals from last sequence in file
            seqLengths.append(seqLen)
            inter = math.floor( seqLen/interval )
            if inter not in lengthInter:
                lengthInter[inter] = 0
            lengthInter[inter] += 1


    # Calclulate N25, N50, and N75 and counts
    seqLengths.sort(reverse=True)
    maxSeq = seqLengths[0]
    minSeq = seqLengths[-1]
    
    # N Stats
    L25 = 0
    N25 = 0
    frac_covered = totalLength = sum(seqLengths)
    while frac_covered > totalLength*0.75:
        N25 = seqLengths[L25]
        L25 += 1
        frac_covered -= N25

    L50 = 0
    N50 = 0
    frac_covered = totalLength = sum(seqLengths)
    while frac_covered > totalLength*0.5:
        N50 = seqLengths[L50]
        L50 += 1
        frac_covered -= N50
    
    L75 = 0
    N75 = 0
    frac_covered = totalLength = sum(seqLengths)
    while frac_covered > totalLength*.25:
        N75 = seqLengths[L75]
        L75 += 1
        frac_covered -= N75
    
    L90 = 0
    N90 = 0
    frac_covered = totalLength = sum(seqLengths)
    while frac_covered > totalLength*.1:
        N90 = seqLengths[L90]
        L90 += 1
        frac_covered -= N90

    # NG Stats
    if genomeSize is None:
        genomeSize = totalLength
    LG25 = 0
    NG25 = 0
    frac_covered = genomeSize
    while frac_covered > genomeSize*0.75:
        NG25 = seqLengths[LG25]
        LG25 += 1
        frac_covered -= NG25

    LG50 = 0
    NG50 = 0
    frac_covered = genomeSize
    while frac_covered > genomeSize*0.5:
        NG50 = seqLengths[LG50]
        LG50 += 1
        frac_covered -= NG50
    
    LG75 = 0
    NG75 = 0
    frac_covered = genomeSize
    while frac_covered > genomeSize*.25:
        NG75 = seqLengths[LG75]
        LG75 += 1
        frac_covered -= NG75
    
    LG90 = 0
    NG90 = 0
    frac_covered = genomeSize
    while frac_covered > genomeSize*.1:
        NG90 = seqLengths[LG90]
        LG90 += 1
        frac_covered -= NG90

    # Print out the results
    print("")
    ints = sorted(lengthInter.keys())
    i = ints[0]
    while i <= ints[-1]:
        if i not in lengthInter:
            lengthInter[i] = 0
        if lengthInter[i] > 0:
            print(f"{i*interval}:{i*interval+interval-1}\t{lengthInter[i]}")
        i += 1
    
    print (f"\nTotal length of sequence:\t{totalLength} bp")
    print (f"Total number of contigs:\t{numSeq}")
    print (f"Max sequence length:\t{maxSeq}")
    print (f"Min sequence length:\t{minSeq}")

    print (f"\nN25 stats:\t\t\t25% of total sequence length is contained in the (L25) {L25} sequences >= {N25} bp")
    print (f"N50 stats:\t\t\t50% of total sequence length is contained in the (L50) {L50} sequences >= {N50} bp")
    print (f"N75 stats:\t\t\t75% of total sequence length is contained in the (L75) {L75} sequences >= {N75} bp")
    print (f"N90 stats:\t\t\t90% of total sequence length is contained in the (L90) {L90} sequences >= {N90} bp")

    print (f"\n*NG Stats using genome length of {genomeSize}.")
    print (f"NG25 stats:\t\t\t25% of total genome length is contained in the {LG25} sequences >= {NG25} bp")
    print (f"NG50 stats:\t\t\t50% of total genome length is contained in the {LG50} sequences >= {NG50} bp")
    print (f"NG75 stats:\t\t\t75% of total genome length is contained in the {LG75} sequences >= {NG75} bp")
    print (f"NG90 stats:\t\t\t90% of total genome length is contained in the {LG90} sequences >= {NG90} bp")

    print (f"\nTotal GC count:\t\t\t{gcCount} bp")
    print (f"GC %:\t\t\t\t{(100.0 * gcCount/totalLength):.2f} %")

    print ("* Without a reference genome we estimate the size using the assembled length.")
    return


## Start main method
if __name__ == "__main__":
    main()

## End of script
