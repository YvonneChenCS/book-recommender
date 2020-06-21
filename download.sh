#!/bin/bash

set -eou pipefail

#wget http://www.gutenberg.org/dirs/GUTINDEX.zip
zcat GUTINDEX.zip > index.txt
