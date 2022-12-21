#!/bin/bash
#
# Compare attributes between DMR++ and Kerchunk
#
for FILE in *.h5; do
    echo $FILE
    python ../zattr.py $FILE.json | sort > $FILE.json.attr;
    python ../oattr.py $FILE.dmrpp | sort > $FILE.dmrpp.attr;
    diff -B $FILE.json.attr $FILE.dmrpp.attr > $FILE.attr.diff
done

for FILE in *.he5; do
    echo $FILE
    python ../zattr.py $FILE.json | sort > $FILE.json.attr;
    python ../oattr.py $FILE.h5.dmrpp | sort > $FILE.dmrpp.attr;
    diff -B $FILE.json.attr $FILE.dmrpp.attr > $FILE.attr.diff
done
