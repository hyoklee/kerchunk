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
 Show that only root group objects are available from zarr.

 See ATL08.py to get the ATL08.zarr input file.
"""

import zarr

z = zarr.open("ATL08.zarr")
print(z.tree())
print(z.info)
print(z.attrs)
