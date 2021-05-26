#!/usr/bin/env bash

../bin/countAssembly.py -i 100 --fasta . > result-path.txt
../bin/countAssembly.py -i 100 --fasta ecoli_Miseq_Assembly.fa > result-Miseq.txt
