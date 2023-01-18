"""
  Compare dataset values between DMR++ and Kerchunk.
"""

import fsspec
import glob
import os
import zarr

from pydap.client import open_url


def print_missing(obj):
    """Print missing dataset in DMR++ file by comparing it to Kerchunk."""
    if type(obj) != zarr.hierarchy.Group:
        a = obj.name
        # print(a)
        a1 = a.replace(" ", "_")
        b = a1.replace(".", "_")
        kl = list(k)
        kstr = str(kl[len(kl) - 1])
        if kstr[0] != "/":
            c = b[1:]
        else:
            c = b
        if c not in k and c[1:] not in k:
            # print(obj)
            print(c)


def print_visitor(obj):
    """This tests dataset value."""
    if type(obj) != zarr.hierarchy.Group:
        a = obj.name
        print(a)
        b = a.replace("/", "_")
        c = b[1:]
        if c in k:
            print(c)
            if dataset[c][:] == za[a][:]:
                print("Yes")
            else:
                print(dataset[c][:])
                print(za[a][:])


# Files that have Int64 will fail Pydap.
skip = [
    "SMAP_L3_SM_P_20150406_R14010_001.h5",
    "SWOT_L2_HR_PIXC_007_483_235R_20220821T102608_20220821T102618_Dx0000_01.nc.h5",
]
for f in sorted(glob.glob("*.h*5")):
    print(f)
    if f in skip:
        continue
    # Collect datasets from OPeNDAP.
    # Use HDF5 handler because Pydap for DMR++ doesn't work.
    url = "http://localhost:8080/opendap/" + f
    tup = os.path.splitext(f)
    if tup[1] == ".he5":
        url = "dap4://localhost:8080/opendap/" + f + ".h5.dmrpp"
    else:
        url = "dap4://localhost:8080/opendap/" + f + ".dmrpp"
    dataset = open_url(url)
    k = dataset.keys()
    # print(k)

    # Open Kerchunk file.
    j = f + ".json"
    mapper = fsspec.get_mapper(
        "reference://",
        fo=j,
        target_protocol="file",
        remote_protocol="file",
    )
    za = zarr.open(mapper, mode="r")
    za.visitvalues(print_missing)
