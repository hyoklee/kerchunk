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
Convert HDF5 to Zarr using DataTree.
"""
import glob
from datatree import DataTree
from datatree.io import open_datatree

skip = [
    "ATL08_20181014084920_02400109_003_01.h5",
    "SMAP_L3_SM_P_20150406_R14010_001.h5",
]

for f in sorted(glob.glob("*.h*5")):
    print(f)
    if f in skip:
        continue
    dt = open_datatree(f)
    dt.to_zarr(f + ".zarr")
