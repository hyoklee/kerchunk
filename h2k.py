#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/12
###########################################################################

"""
Generate Kerchunk JSON files from HDF5 files.
"""
import glob
import kerchunk.hdf
import fsspec
import time
import ujson

so = dict(anon=True, default_fill_cache=False, default_cache_type='first')
fs = fsspec.filesystem('')  #local file system to save final jsons to

for f in glob.glob('*.h*5'):
    print(f)
    with fsspec.open(f, **so) as inf:
        start = time.time()
        h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, f, inline_threshold=100)
        end = time.time()
        outf = f+'.json'
        with fs.open(outf, 'wb') as fo:
            fo.write(ujson.dumps(h5chunks.translate()).encode());     
            print(end - start)
