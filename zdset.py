#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/14
###########################################################################

"""
Read a dataset from Kerchunk using Zarr.
Compare the dataset values from DataTree-converted Zarr.
"""

import kerchunk.hdf
import fsspec
import time
import ujson
import xarray as xr
import zarr

backend_args = {"consolidated": False, "storage_options": {"fo":'ATL08.json'}}

mapper = fsspec.get_mapper(
    'reference://',
    fo='ATL08.json',
    target_protocol='file',
    remote_protocol='file',
)

za = zarr.open(mapper, mode='r')
print(za['ds_geosegments'][:])

z5 = zarr.open('ATL08dt.h5.zarr')
print(z5['ds_geosegments'][:])
