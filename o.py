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
Read all datasets from all files using DMR++.
"""

import os
import glob
from pydap.client import open_url

# These large datasets will make program hang.
skip = ["analysed_sst", "analysis_error", "mask", "sea_ice_fraction"]

# Docker mounts /tmp/dmrpp and generates DMR++ there.
for f in sorted(glob.glob("/tmp/dmrpp/*.dmrpp")):
    ## DAP2
    # url = 'http://localhost:8080/opendap/' + os.path.basename(f)

    ## DAP4
    url = "dap4://localhost:8080/opendap/" + os.path.basename(f)

    print(url)
    dataset = open_url(url)
    print(dataset)
    for i in dataset.keys():
        print(i)
        if i not in skip:
            d = dataset[i][:]
            print(d)
        else:
            print("Skipping " + i)
