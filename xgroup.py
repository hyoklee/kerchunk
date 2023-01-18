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
Read a specific group using xarray from Kerchunk.
"""

import glob
import xarray as xr

for f in glob.glob("ATL08*.h*5.json"):
    print(f)
    backend_args = {"consolidated": False, "storage_options": {"fo": f}}
    ds = xr.open_dataset(
        "reference://",
        engine="zarr",
        backend_kwargs=backend_args,
        group="/METADATA/AcquisitionInformation/platform",
    )
    print(ds)
