#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/15
###########################################################################

"""
Read a dataset from Kerchunk using Zarr.
Compare the dataset values from DataTree-converted Zarr.
"""

import fsspec
import glob
import zarr

skip_STARL2P = ['/geostationary', '/crs', '/dt_analysis', '/l2p_flags',
                '/l3s_sst_reference', '/quality_level',
                '/satellite_zenith_angle', '/sea_surface_temperature',
                '/sses_bias', '/sses_standard_deviation', '/sst_count',
                '/sst_dtime']
skip_STARL3S = ['/sst_source', '/wind_speed']
skip_AMSR = ['/HDFEOS INFORMATION/CoreMetadata.0',
             '/HDFEOS INFORMATION/StructMetadata.0']
skip_ATL08 = ['/ancillary_data/release', '/ancillary_data/version']
skip_OMI = ['/HDFEOS INFORMATION/ArchivedMetadata.0']
skip =  skip_STARL2P + skip_STARL3S + skip_AMSR + skip_ATL08 + skip_OMI

for f in sorted(glob.glob('VNP*.h*5.json')):
    print(f)
    mapper = fsspec.get_mapper(
        'reference://',
        fo=f,
        target_protocol='file',
        remote_protocol='file',
    )
    za = zarr.open(mapper, mode='r')
    def print_visitor(obj):
        if type(obj) != zarr.hierarchy.Group:
            a = obj.name
            if a in skip:
                print('Skipping '+a)
            else:
                print(a)
                print(za[a][:])
    za.visitvalues(print_visitor)
    
# z5 = zarr.open('ATL08dt.h5.zarr')
# print(z5['ds_geosegments'][:])
