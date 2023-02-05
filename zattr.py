#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022-2023 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2023/02/05
###########################################################################

"""
Read all attribute from Kerchunk using Zarr.
"""

import fsspec
import sys
import zarr


def print_visitor(obj):
    # for a in obj.attrs:
    #    print(a)
    if type(obj) == zarr.hierarchy.Group or type(obj) == zarr.hierarchy.Array:
        a = obj.name
        if obj.attrs.keys():
            for k in obj.attrs.keys():
                if k != "_ARRAY_DIMENSIONS":
                    print(a + ":" + k + "=" + str(obj.attrs[k]))


if __name__ == "__main__":
    f = sys.argv[1]
    # print(f)
    mapper = fsspec.get_mapper(
        "reference://",
        fo=f,
        target_protocol="file",
        remote_protocol="file",
    )
    za = zarr.open(mapper, mode="r")
    # Print global attributes
    # print(za.attrs.keys())
    for k in za.attrs.keys():
        print(":" + k + "=" + str(za.attrs[k]))
    za.visitvalues(print_visitor)
