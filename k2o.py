#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (C) 2023 The HDF Group
#
# Author: Hyo-Kyung Lee (hyoklee@hdfgroup.org)
#
# Last Update: 2023/01/24
###########################################################################

"""
Generate DMR++ from Kerchunk.

Implementation Idea

1. Read Kerchunk file using fsspec+zarr.
2. Iterate using za.visitvalues()
2.1 Parse offset/length using a generic json parser.
3. Build XML using etree.

"""
import os
import sys
import json
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
        self.json = None

    def get_obj(self, obj):
        if type(obj) == zarr.hierarchy.Group:
            p = obj.name
            path = os.path.normpath(p)
            l = path.split(os.sep)
            l.pop(0)

            i = 0
            c = None
            for n in l:
                if i == 0:
                    c = self.write_group(self.root, n)
                else:
                    g = self.write_group(c, n)
                    c = g
                i = i + 1
        else:  # Dataset
            n = obj.name
            print(n)
            d = self.write_dset(n)
            for key in self.json["refs"].keys():
                if key.startswith(obj.path):
                    if not (key.endswith(".zarray") or key.endswith(".zattrs")):
                        print(key)
                        v = self.json["refs"][key]
                        print(v)
                        offset = v[1]
                        nbytes = v[2]
                        pos = "[0,0]"  # Parse /0.0 from key later.
                        self.write_chunks(d, offset, nbytes, pos)

    def write_dset(self, n):
        d = etree.SubElement(self.root, "Int32")
        d.set("name", n)
        return d

    def write_chunks(self, p, offset, nbytes, pos):
        c = etree.SubElement(p, "{" + self.ns + "}chunks")
        c.set("byteOrder", "LE")
        s = etree.SubElement(c, "{" + self.ns + "}chunk")
        s.set("offset", str(offset))
        s.set("nBytes", str(nbytes))
        s.set("chunkPositionInArray", pos)

    def write_group(self, e, n):
        f = e.find("Group[@name='" + n + "']")
        if f is not None:
            return f
        else:
            g = etree.SubElement(e, "Group")
            _n = n.replace(" ", "_")
            g.set("name", _n)
            return g

    def read_zarr(self):
        with open(self.z) as json_file:
            try:
                self.json = json.load(json_file)
            except ValueError:
                print("ERROR:Invalid json file " + self.z)

        mapper = fsspec.get_mapper(
            "reference://",
            fo=self.z,
            target_protocol="file",
            remote_protocol="file",
        )
        za = zarr.open(mapper, mode="r")
        print(za)
        # Write global attributes.
        self.write_attrs(za, self.root)

        # Visit Zarr items.
        za.visitvalues(self.get_obj)

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

    def write_attrs(self, za, g):
        for k in za.attrs.keys():
            a = etree.SubElement(self.root, "Attribute")
            a.set("name", k)
            v = etree.SubElement(a, "Value")
            if isinstance(za.attrs[k], str):
                a.set("type", "String")  # See [1].
            elif isinstance(za.attrs[k], int):
                a.set("type", "Int64")  # No Uint64 in NASA samples
            else:
                a.set("type", "Float64")
            v.text = str(za.attrs[k])


if __name__ == "__main__":

    d = DMR(sys.argv[1])
    d.set_root()
    d.read_zarr()
    d.write()

# Reference
# 1. https://github.com/zarr-developers/zarr-python/issues/156
