#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/16
###########################################################################

"""
Convert a flattened CF-compliant netCDF-4 into Zarr via Kerchunk.

NCZarr-enabled ncdump will fail on the converted file.
"""

import kerchunk.hdf
import fsspec
import time
import ujson
import xarray as xr

# An input file from Hyrax fileout_netcdf
f = 'ATL08_20210114234518_03361001_004_01.h5.nc4' 
outf = f+'.json'
     
so = dict(anon=True, default_fill_cache=False, default_cache_type='first')

fs2 = fsspec.filesystem('')  # local file system to save Kerchunk JSON

with fsspec.open(f, **so) as inf:
     start = time.time()
     h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, f, inline_threshold=100)
     end = time.time()
     with fs2.open(outf, 'wb') as fout:
         fout.write(ujson.dumps(h5chunks.translate()).encode());     
     print(end - start)

# Read Kerchunk back.     
backend_args = {"consolidated": False, "storage_options": {"fo":outf}}
ds = xr.open_dataset(
    "reference://", engine="zarr",
    backend_kwargs=backend_args
)
print(ds)

# Write Zarr.
ds.to_zarr(f+'.zarr')
