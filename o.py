#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2022 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2022/12/14
###########################################################################
import os
import glob
from pydap.client import open_url

for f in sorted(glob.glob('/tmp/dmrpp/*.dmrpp')):

    ## DAP2
    #url = 'http://localhost:8080/opendap/' + os.path.basename(f)
    
    ## DAP4
    url = 'dap4://localhost:8080/opendap/' + os.path.basename(f)
    print(url)
    dataset = open_url(url)
    print(dataset)
    for i in dataset.keys():
        print(i)
        d = dataset[i][:]
        print(d)
