#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2023 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2023/01/18
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
        self.h5n = os.path.split(self.h5)[1]  # Remove .json.
        self.out = self.z + ".dmrpp"
        etree.register_namespace("dmrpp", self.ns)

    def read_zarr(self):
        mapper = fsspec.get_mapper(
            "reference://",
            fo=self.z,
            target_protocol="file",
            remote_protocol="file",
        )
        za = zarr.open(mapper, mode="r")
        # Print global attributes
        for k in za.attrs.keys():
            a = etree.SubElement(self.root, "Attribute")
            a.set("name", k)
            b = etree.SubElement(a, "Value")
            if isinstance(za.attrs[k], str):
                a.set("type", "String")  # See [1].
            elif isinstance(za.attrs[k], int):
                a.set("type", "Int64")  # No Uint64 in NASA samples
            else:
                a.set("type", "Float64")
            b.text = str(za.attrs[k])

    def set_root(self):
        self.root.set("xmlns", "http://xml.opendap.org/ns/DAP/4.0#")
        self.root.set("dapVersion", "4.0")
        self.root.set("dmrVersion", "1.0")
        self.root.set("name", self.h5n)
        self.root.set("{" + self.ns + "}href", "file:///" + self.h5)
        self.root.set("{" + self.ns + "}version", "3.20.13-240")

    def write(self):
        et = etree.ElementTree(self.root)
        et.write(
            self.out,
            encoding="ISO-8859-1",
            pretty_print=True,
            xml_declaration=True,
        )


if __name__ == "__main__":

    d = DMR(sys.argv[1])
    d.set_root()
    d.read_zarr()
    d.write()

# Reference
# 1. https://github.com/zarr-developers/zarr-python/issues/156
