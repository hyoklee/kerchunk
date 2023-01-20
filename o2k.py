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
Generate Kerchunk from DRM++.

Implementation Idea

 1. Create kerchunk/dmr.py like kerchunk/hdf.py.
 2. dmr = kerchunk.dmr.SingleDMRToZarr(inf, f, inline_threshold=0)
 3. Generate Zarr file from dmr.translate()

"""

import sys
import zarr
import ujson
import fsspec
import kerchunk

import lxml.etree as etree

from typing import Union
from kerchunk.utils import _encode_for_JSON


class SingleDMRToZarr:
    """Translate the content of DMR++ into Zarr metadata."""

    def __init__(self, dmr):
        self.store = {}
        self._zroot = zarr.group(store=self.store, overwrite=True)
        self._dmr = dmr

    def translate(self):
        # zgrp = self._zroot.create_group("test")
        # self._transfer_attrs(self._dmr, self._zroot)
        store = _encode_for_JSON(self.store)
        # self._transfer_attrs(h5obj, zgrp)
        return {"version": 1, "refs": store}

    def _transfer_attrs(
        self,
        attrs,
        zobj: Union[zarr.Array, zarr.Group],
    ):
        zobj.attrs[0] = [attrs]


class DMRParser(object):

    """DMR parser class"""

    def __init__(self, DMR_file):
        """Constructor

        @param DMR_file: OPeNDAP Hyrax DMR++ file name
        """

        self.xml_file = DMR_file
        self.depth = 0
        self.tree = None
        self.last = "group"
        self.z = None
        # See [1] for type map.
        # UByte is from legacy DAP4 schema and example.
        self.type_hash_map = {
            "Byte": "uint8",
            "UByte": "uint8",
            "Int8": "int8",
            "UInt8": "uint8",
            "Int16": "int16",
            "UInt16": "uint16",
            "Int32": "int32",
            "UInt32": "uint32",
            "Int64": "int64",
            "UInt64": "uint64",
            "Url": "string",
            "Float32": "float32",
            "Float64": "float64",
            "String": "string",
            "Structure": "compound",
        }

        self.use_dimscale = True

        try:
            self.tree = etree.parse(self.xml_file).getroot()

        except etree.XMLSyntaxError as err:
            print("The DMR file is not valid:")
            print(self.xml_file)
            print(err)
            return None
        except IOError as err:
            print("ERROR:Can't read the DMR file :" + self.xml_file)
            print(err)
            return None

        self.schema = "{http://xml.opendap.org/ns/DAP/4.0#}"

        self.group_stack = ["/"]
        self.attr_stack = []
        self.dset_stack = []
        self.dims = {}
        self.dimscales = {}

    def get_ascii_string(self, _str):
        """Filter non-printable characters in DMR."""
        flag = False
        for c in _str:
            if c not in string.printable:
                flag = True
        if flag:
            print("WARNING:non-printable character in ")
            print(_str.encode("ascii", errors="replace"))
            a = filter(lambda x: x in string.printable, _str)
            return a
        else:
            return _str

    def get_shape_str(self, shape):
        """Format shape. DMR shape can be empty."""
        str_shape = ""
        if shape == "":
            # Scalar is now fine.
            # Do not give warning or change it to 1.
            # print "WARNING:Variable shape is null."
            str_shape = ""
        else:
            for dim in shape.split():
                if dim in self.dims.keys():
                    str_shape = str_shape + str(self.dims[dim]) + ","
                else:  # DMR shape can be numerals.
                    str_shape = str_shape + str(dim) + ","
            str_shape = str_shape[:-1]
        return str_shape

    def get_unsigned_attr(self, attr_node, dtype, value):
        """DMR attribute may contain isUnsigned='true' attribute for unsigned
        type attribute.
        """
        cdtype = dtype

        # if value == '3.4028235E38':
        # h5py json checker can't handle it.
        #    value = '3.4028E38'
        cvalue = value

        if (
            "isUnsigned" in attr_node.keys()
            and attr_node.attrib["isUnsigned"] == "true"
        ):
            if value[0] == "[" and value[-1] == "]":
                cvalue = ""
                value_list = ast.literal_eval(value)
                for item in value_list:
                    cdtype, tvalue = self.get_unsigned_dtype_value(dtype, str(item))
                    cvalue = cvalue + str(tvalue) + ","
                cvalue = cvalue[:-1]
                cvalue = "[" + cvalue + "]"
            else:
                cdtype, cvalue = self.get_unsigned_dtype_value(dtype, value)
        return cdtype, cvalue

    def get_unsigned_dtype_dset(self, dset_node, dtype):
        """DMR dataset may contain _Unsigned='true' attribute for unsigned
        type dataset.
        """
        cdtype = dtype
        for node in dset_node.getchildren():
            if node.tag == self.schema + "attribute":
                if (
                    node.attrib["name"] == "_Unsigned"
                    and node.attrib["value"] == "true"
                ):
                    cdtype = "u" + dtype
        return cdtype

    def get_unsigned_dtype_value(self, dtype, value):
        """Convert signed value into unsigned value."""
        cdtype = "u" + dtype
        str_eval = "np." + cdtype + "(" + value + ")"
        cvalue = str(eval(str_eval))
        return cdtype, cvalue

    def get_value_str(self, value):
        """Format value."""
        str_value = ""
        if value == []:
            print("WARNING:Value is empty.")
        else:
            if len(value) > 1:
                str_value = str(value)
            else:
                str_value = str(value[0])
        return str_value

    def parse_content(self, z):
        """Parses the DMR."""
        self.z = z._zroot
        self.depth = 1
        # DMR's schema can vary from 3.2, 3.3 to 4.0.
        # Determine it from XML file.
        self.schema = self.tree.tag.split("}")[0] + "}"
        self.recursive_walk(self.tree, self.depth)

    def select_group(self):
        """Determine the right level of group."""
        i = len(self.group_stack) - self.depth
        # print('select_group():i='+str(i))

        # Select the last group in the stack.
        while (i > 0) and (len(self.group_stack) > 1):
            self.group_stack.pop()
            i = i - 1
            item = self.group_stack[-1]
            # print(item)

    def get_path(self):
        """Get the path from group stack."""
        path = ""
        for i in self.group_stack:
            if i != "/":
                path += "/" + i
        # print(path)
        return path

    def get_value(self, node):
        """Find value tag from node's children and returns its value."""
        v = []
        for c in node.getchildren():
            if c.tag == self.schema + "value" or c.tag == self.schema + "Value":
                v.append(c.text)
        if v == []:
            print(
                "WARNING:No value/Value tag is found for " + node.attrib["name"] + "."
            )
        return v

    def get_type(self, node):
        """Find type tag from node's children and returns its value."""
        for c in node.getchildren():
            for key in self.type_hash_map:
                if c.tag == self.schema + key:
                    value = self.type_hash_map[key]
                    return value

    def create_dataset_dap4_array(self, node, key):
        """Create simple dataset for DAP 4.0."""
        self.select_group()
        dname = node.attrib["name"]
        return dname

    def get_orig_gname(self, g):
        """Replace _ with white space."""
        l = [
            "Data_Fields",
            "Geolocation_Fields",
            "HDFEOS_INFORMATION",
            "Northern_Hemisphere",
            "Southern_Hemisphere",
        ]
        h = g
        if g in l:
            h = g.replace("_", " ")
        return h

    def recursive_walk(self, root_node, depth):
        """This recursive function traverse the XML document using the
        ElementTree API; all nodes are stored in a tree-like structure.

        If a 'Group' tag is found, the attribute 'ID' is inserted in a stack;
        its node will have this value as prefix for the file name.

        @param root_node: lxml root node of the map file
        @param depth: used to keep track of the recursion level, 0 on the root.
        """

        """
        # For debugging.
        print('recursiv_walk():')
        print('stack length='+str(len(self.group_stack)))
        m='d='+str(depth)+' self.d='+str(self.depth)+' self.last='+self.last
        print(m)
        print(self.group_stack)
        """

        self.depth = depth

        for node in root_node.getchildren():
            # print(node.tag)
            # Attribute
            if node.tag == self.schema + "Attribute":
                # print(node.attrib['name'])
                if "type" in node.keys():
                    if node.attrib["type"] != "Container":
                        dtype = self.type_hash_map[node.attrib["type"]]
                    else:
                        dtype = "container"
                        self.dset_stack = []
                else:
                    dtype = "string"
                name = node.attrib["name"]
                self.select_group()
                if dtype == "container":
                    # print('Attribute Container:'+name)
                    self.attr_stack.append(name)
                    self.last = "acon"
                else:
                    val = self.get_value(node)
                    value = self.get_value_str(val)
                    m = node.attrib["name"] + "=" + value
                    lg = len(self.group_stack)
                    if self.depth > lg:
                        if len(self.dset_stack) > 0:
                            m = self.get_path() + "/" + self.dset_stack[-1] + ":" + m
                        else:
                            m = ""  # Ignore attribute container
                    else:
                        m = self.get_path() + ":" + m
                    print(m)

            # Group
            if node.tag == self.schema + "Group":
                if "name" in node.keys():
                    gname = node.attrib["name"]
                    self.z.create_group(self.get_path() + "/" + gname)
                else:
                    print("WARNING:Group tag has no name.")
                    gname = "noname"

                gname = self.get_orig_gname(gname)
                # print(gname)
                self.select_group()

                self.attr_stack = []
                self.dset_stack = []

                self.group_stack.append(gname)
                self.last = "group"

            # Array in DAP 4.0
            for key in self.type_hash_map:
                if node.tag == self.schema + key:
                    dset = self.create_dataset_dap4_array(node, key)
                    if dset:
                        self.dset_stack.append(dset)
                        self.last = "variable"

            # Dimension.
            if node.tag == self.schema + "Dimension":
                path = self.get_path()
                if "size" in node.attrib.keys():
                    length = node.attrib["size"]
                else:
                    print("ERROR:dimension tag has no size.")
                    length = 1

                self.dims[path + node.attrib["name"]] = length

                if self.use_dimscale:
                    if self.last != "group":
                        self.select_group()
                    self.dimscales[path + node.attrib["name"]] = length
                self.last = "dimension"

            if len(node) > 0:
                self.recursive_walk(node, self.depth + 1)
                self.depth = self.depth - 1


if __name__ == "__main__":
    # unittest.main()

    parser = DMRParser(sys.argv[1])
    dmr = SingleDMRToZarr(parser.xml_file)
    parser.parse_content(dmr)

    # Save Kerchunk to local file system.
    fs = fsspec.filesystem("")
    outf = parser.xml_file + ".json"
    with fs.open(outf, "wb") as fo:
        fo.write(ujson.dumps(dmr.translate()).encode())

# Reference
#
# [1] http://docs.opendap.org/index.php/DAP4:_Specification_Volume_1#Appendix_1._DAP4_DMR_Syntax_as_a_RELAX_NG_Schema
