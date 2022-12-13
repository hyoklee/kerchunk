#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/13
###########################################################################

"""
Create Zarr and netCDF-4 using xarray and kerchunk.
Input data product is ATL08.
"""

import kerchunk.hdf
import fsspec
import time
import ujson
import xarray as xr

so = dict(anon=True, default_fill_cache=False, default_cache_type='first')

## Relative path works fine.
f = './data/ATL08_20181014084920_02400109_003_01.h5'
## Full path also works.
# f = 'file:///Users/hyoklee/src/kerchunk/data/ATL08_20181014084920_02400109_003_01.h5'
## IPFS works fine, too.
# f = 'ipfs://QmVZc4TzRP7zydgKzDX7CH2JpYw2LJKkWBm6jhCfigeon6'
fs2 = fsspec.filesystem('')  #local file system to save final jsons to

with fsspec.open(f, **so) as inf:
     start = time.time()
     h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, f, inline_threshold=100)
     end = time.time()
     outf = 'ATL08.json'
     with fs2.open(outf, 'wb') as f:
         f.write(ujson.dumps(h5chunks.translate()).encode());     
     print(end - start)
     
backend_args = {"consolidated": False, "storage_options": {"fo":'ATL08.json'}}
ds = xr.open_dataset(
    "reference://", engine="zarr",
    backend_kwargs=backend_args
)
print(ds)

# It will store only root group and attributes.
ds.to_zarr("ATL08.zarr")
ds.to_netcdf("ATL08.nc")
