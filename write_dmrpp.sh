#!/bin/bash
# This script will write each output file as a sidecar file into 
# the same directory as its associated input granule data file.

# The target directory to search for data files 
target_dir=/usr/share/hyrax
echo "target_dir: ${target_dir}";

# Search the target_dir for names matching the regex \*.h5 
for infile in `find "${target_dir}" -name \*.h5`
do
    echo " Processing: ${infile}"

    infile_base=`basename "${infile}"`
    echo "infile_base: ${infile_base}"

    bes_dir=`dirname "${infile}"`
    echo "    bes_dir: ${bes_dir}"

    outfile="${infile}.dmrpp"
    echo "     Output: ${outfile}"

    get_dmrpp -b "${bes_dir}" -c /etc/bes/bes.conf -o "${outfile}" -u "file://${infile}" "${infile_base}"
done
