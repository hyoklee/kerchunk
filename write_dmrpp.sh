#!/bin/bash
# This script will write each output file as a sidecar file into 
# the same directory as its associated input granule data file.

# The target directory to search for data files 
target_dir=/usr/share/hyrax
echo "target_dir: ${target_dir}";

# Enable CF option.
echo "H5.EnableCF=true" > site.conf

# Search the target_dir for names matching the regex \*.h5 
for infile in `find "${target_dir}" -name \*.h5`
do
    echo " Processing: ${infile}"

    infile_base=`basename "${infile}"`
    echo "infile_base: ${infile_base}"

    bes_dir=`dirname "${infile}"`
    echo "    bes_dir: ${bes_dir}"

    outfile="${infile}.cf.dmrpp"
    echo "     Output: ${outfile}"

    # -c option doesn't work.
    # get_dmrpp -c /etc/bes/bes.conf -b "${bes_dir}" -o "${outfile}" -u "file://${infile}" "${infile_base}"
    get_dmrpp -s site.conf -b "${bes_dir}" -o "${outfile}" -u "file://${infile}" "${infile_base}"
done
