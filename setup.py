from setuptools import setup

# read long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MetaomeStats',
    version='0.4',
    author='Jose Luis Figueroa III, Richard Alan White III',
    author_email='jlfiguer@uncc.edu',
    url='https://github.com/raw-lab/metaome_stats',
    description='Scripts for calculating statistics from FASTA sequences',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['countAssembly/bin/countAssembly.py'],
    license="MIT License", # metadata
    platforms=['Unix'], # metadata
    classifiers=[ # This is the new updated way for metadata, but old way seems to still be used in some of the output
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
