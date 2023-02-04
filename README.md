

# Kerchunk Study

[![test](https://github.com/hyoklee/kerchunk/actions/workflows/ATL08.yml/badge.svg)](https://github.com/hyoklee/kerchunk/actions/workflows/ATL08.yml)
[![codespell](https://github.com/hyoklee/kerchunk/actions/workflows/codespell.yml/badge.svg)](https://github.com/hyoklee/kerchunk/actions/workflows/codespell.yml)
[![black](https://github.com/hyoklee/kerchunk/actions/workflows/black.yml/badge.svg)](https://github.com/hyoklee/kerchunk/actions/workflows/black.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

  Test Kerchunk using real NASA HDF5 [data](data) products.
  Compare it to DMR++.

## Study Report
* Read [Wiki](https://github.com/hyoklee/kerchunk/wiki/).

## Source Codes
* [attr.sh](attr.sh): Compare attributes between DMR++ and Kerchunk.
* [h2k.py](h2k.py): Generate Kerchunk from HDF5.
* [h2z.py](h2z.py): Generate Zarr from HDF5 using DataTree.
* [o.py](o.py): Read all DMR++ datasets from HDF5.
* [o2k.py](o2k.py): Generate Kerchunk from DMR++.
* [oz.py](oz.py): Compare DMR++ & Kerchunk datasets from HDF5.
* [wo.sh](wo.sh): Write CF-enabled DMR++ from HDF5.
* [zdset.py](zdset.py): Read all Kerchunk datasets from HDF5.
* [zgroup.py](zgroup.py): Compare Kerchunk & DataTree-generated Zarr groups.
