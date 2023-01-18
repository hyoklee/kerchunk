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
Create Zarr using DataTree.

HDF5 to Zarr works.
Kerchunk to Zarr fails.

"""
import fsspec
import zarr

import xarray as xr

from datatree import DataTree
from datatree.io import open_datatree
from datatree.testing import assert_equal
from datatree.tests import requires_zarr
from sys import stdout

backend_args = {"consolidated": False, "storage_options": {"fo": "ATL08.json"}}

mapper = fsspec.get_mapper(
    "reference://",
    fo="ATL08.json",
    target_protocol="file",
    remote_protocol="file",
)

## Test Zarr with mapper.
za = zarr.open(mapper, mode="r")
print(za.keys())
print(za.tree())

# za = zarr.open_consolidated(mapper, mode='r')
#! KeyError: '.zmetadata'

g = zarr.open_group(mapper, mode="r")
print(g.keys())
print(g.tree())

if g.keys() == za.keys():
    print("keys:yes")

if g.tree() == za.tree():
    print("tree:yes")
else:
    print("tree:no")

## Read a specific dataset.
print(za["ancillary_data/end_orbit"][:].tobytes())
print(za["ancillary_data/end_orbit"][:])

##  The 'out' becomes 'None'.
# out = zarr.load(za, zarr_version=2, path=za)
## Thus, this will not work.
# out.save('ATL08dt.zarr')

## Test Zarr with Xarray.
## Xarray dataset doesn't work.
ds = xr.open_dataset("reference://", engine="zarr", backend_kwargs=backend_args)

# za = zarr.open(ds, mode='r')
#! zarr.errors.PathNotFoundError: nothing found at path ''


## Test DataTree.

## DataTree can't use Kerchunk JSON.
# dt = DataTree.from_dict('ATL08.json')
#! AttributeError: 'str' object has no attribute 'pop'

# dt = DataTree.from_dict(za)
#! zarr.errors.ReadOnlyError: object is read-only


##  These save only root group and dimension variables.
# zarr.save('ATL08t.zarr', za)
# zarr.save_group('ATL08t.zarr', za)

# store = zarr.DirectoryStore('ATL08dt.zarr')
# g = store.group()

##  Throws an error.
# zarr.copy_store(za, store, log=stdout)
# zarr.copy_all(za, g, log=stdout)
# g = zarr.open_group(za)
# print(g)


dt = open_datatree("data/ATL08_20181014084920_02400109_003_01.h5")
# print(dt.keys())
dt.to_zarr("ATL08dt.h5.zarr")

# dt = open_datatree(g, engine='zarr', mode='r')
# dt = open_datatree(za, engine='zarr', mode='r')
#! zarr.errors.GroupNotFoundError: group not found at path ''

## To avoid the above error, use this.
dt = open_datatree(mapper, engine="zarr", mode="r", backend_kwargs=backend_args)
# print(dt.keys())
dt.to_zarr("ATL08dt.kerchunk.zarr")
#! ValueError: When changing to a larger dtype, its size must be a divisor of
#! the total size in bytes of the last axis of the array.
