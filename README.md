# Kerchunk Study

  Test Kerchunk against real NASA HDF5 data products.
  Compare it to DMR++.

## Study Report
* Read [Wiki](https://github.com/hyoklee/kerchunk/wiki/).

## Source Codes
* [attr.sh](attr.sh): Compare attributes between DMR++ and Kerchunk.
* [h2k.py](h2k.py): Generate Kerchunk from HDF5.
* [h2z.py](h2z.py): Generate Zarr from HDF5 using DataTree.
* [o.py](o.py): Read all DMR++ datasets from HDF5.
* [oz.py](oz.py): Compare DMR++ & Kerchunk datasets from HDF5.
* [wo.sh](wo.sh): Write CF-enabled DMR++ from HDF5.
* [zdset.py](zdset.py): Read all Kerchunk datasets from HDF5.
* [zgroup.py](zgroup.py): Compare Kerchunk & DataTree-generated Zarr groups.
