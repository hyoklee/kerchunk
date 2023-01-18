#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022-2023 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2023/01/12
###########################################################################

"""
Compare trees from two Zarr files.

  1. Kerchunk reference JSON
  2. DataTree-generated Zarr from HDF5 (h2z.py)

"""

import difflib
import fsspec
import glob
import zarr

# DataTree gives errors during conversion for this HDF5 file.
skip = [
    "ATL08_20181014084920_02400109_003_01.h5.json",
    "SMAP_L3_SM_P_20150406_R14010_001.h5.json",
    "no_dset.h5.json",
]

# Use the following command's output for the problematic files.
#
# $ h5ls -r ATL08_20181014084920_02400109_003_01.h5 | grep Group | cut -d ' ' -f1
# Compare it with the following function's output.
def print_visitor(obj):
    if type(obj) == zarr.hierarchy.Group:
        a = obj.name
        print(a)


for f in sorted(glob.glob("*5.json")):
    print(f)
    mapper = fsspec.get_mapper(
        "reference://",
        fo=f,
        target_protocol="file",
        remote_protocol="file",
    )
    za = zarr.open(mapper, mode="r")
    if f in skip:
        za.visitvalues(print_visitor)
        continue

    fb = f[:-5] + ".zarr"
    print(fb)
    zb = zarr.open(fb, mode="r")

    if str(za.tree()) == str(zb.tree()):
        print("Y")
    else:
        print("N")
        # print(za.tree())
        # print(zb.tree())
        diff = "\n" + "\n".join(
            difflib.ndiff(str(za.tree()).split("\n"), str(zb.tree()).split("\n"))
        )
        print(diff)
