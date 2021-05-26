# Metaome Stats: scripts for calculating statistics from FASTA sequences

================================================

## Installing

- pip installation
`pip install MetaomeStats`

- conda installation
`conda install -c bioconda MetaomeStats`

- source (github)

```bash
git clone https://github.com/raw-lab/metaome_stats
cd rhea
python setup.py
```

-------

## Usage examples

```bash
countAssembly.py -i 100 --fasta ecoli_Miseq_Assembly.fa
```

Main options:
```
usage: countAssembly.py -i INTERVAL -f FASTA [-r REF] [-s SIZE] [-h]

required arguments:
  -i INTERVAL, --interval INTERVAL
                        interval size in # of residues
  -f FASTA, --fasta FASTA
                        fasta file or folder

optional arguments:
  -r REF, --ref REF     reference genome
  -s SIZE, --size SIZE  reference genome size
  -h, --help
```

-------

## Input formats

- FASTA files without quality scores (.fasta, .fa, .fna, .ffn format)

-------

## Citing Metaome Stats

If you are publishing results obtained using Metaome Stats, please cite: 

CONTACT

-------
The informatics point-of-contact for this project is [Dr. Richard Allen White III](https://github.com/raw-lab).<br />
If you have any questions or feedback, please feel free to get in touch by email. <br />
Dr. Richard Allen White III - rwhit101@uncc.edu.  <br />
Jose Figueroa - jlfiguer@uncc.edu.  <br /> 
Or [open an issue](https://github.com/raw-lab/metaome_stats/issues).
