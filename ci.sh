#!/bin/bash
git clone https://github.com/OPENDAP/hyrax
cd hyrax
source ./spath.sh
./hyrax_clone.sh
./hyrax_build.sh
ls
ls build/bin
