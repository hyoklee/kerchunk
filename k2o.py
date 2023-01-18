#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2023 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2023/01/17
###########################################################################

"""
Generate DMR++ from Kerchunk.

Implementation Idea

1. Read Kerchunk file using fsspec+zarr.
2. Iterate using za.visitvalues()
3. Build XML using etree.

"""
import sys
import zarr
import fsspec
import lxml.etree as etree

etree.register_namespace('dmrpp', 'http://xml.opendap.org/dap/dmrpp/1.0.0#')

root = etree.Element('Dataset')
root.set('xmlns', 'http://xml.opendap.org/ns/DAP/4.0#')
root.set('dapVersion', '4.0')
root.set('dmrVersion', '1.0')
root.set('name', 'output.xml')
root.set('{http://xml.opendap.org/dap/dmrpp/1.0.0#}href', 'file:///usr/share/hyrax/20020602090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.h5')
root.set('{http://xml.opendap.org/dap/dmrpp/1.0.0#}version', '3.20.13-240')
et = etree.ElementTree(root)
et.write('output.xml', encoding='ISO-8859-1',
         pretty_print=True, xml_declaration=True)
