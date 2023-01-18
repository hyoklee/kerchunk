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
import os
import sys
import zarr
import fsspec
import lxml.etree as etree


class DMR:
    """Build XML tree from Zarr metadata."""

    def __init__(self, z):
        self.ns = "http://xml.opendap.org/dap/dmrpp/1.0.0#"
        self.root = etree.Element("Dataset")
        self.z = z
        self.h5 = os.path.splitext(z)[0]  # Remove .json.
        etree.register_namespace("dmrpp", self.ns)

    def set_root(self):
        self.root.set("xmlns", "http://xml.opendap.org/ns/DAP/4.0#")
        self.root.set("dapVersion", "4.0")
        self.root.set("dmrVersion", "1.0")
        self.root.set("name", "output.xml")
        self.root.set(
            "{http://xml.opendap.org/dap/dmrpp/1.0.0#}href", "file:///" + self.h5
        )
        self.root.set("{" + self.ns + "}version", "3.20.13-240")

    def write(self):
        et = etree.ElementTree(self.root)
        et.write(
            self.h5 + ".dmrpp",
            encoding="ISO-8859-1",
            pretty_print=True,
            xml_declaration=True,
        )


if __name__ == "__main__":

    d = DMR(sys.argv[1])
    d.set_root()
    d.write()
