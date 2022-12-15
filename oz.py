"""
  Compare dataset values between DMR++ and Kerchunk.
"""

import fsspec
import glob
import zarr

from pydap.client import open_url
for f in sorted(glob.glob('*.h*5')):
    print(f)
    # Collect datasets from OPeNDAP.
    # Use HDF5 handler because Pydap for DMR++ doesn't work.
    url = 'http://localhost:8080/opendap/'+f
    dataset = open_url(url)
    k = dataset.keys()
    # print(k)
    # Open Kerchunk file.
    j = f+'.json'
    mapper = fsspec.get_mapper(
        'reference://',
        fo=j,
        target_protocol='file',
        remote_protocol='file',
    )
    za = zarr.open(mapper, mode='r')
    def print_visitor(obj):
        if type(obj) != zarr.hierarchy.Group:
            a = obj.name
            print(a)
            b = a.replace('/', '_')
            c = b[1:]
            if c in k:
                print(c)
                if dataset[c][:] == za[a][:]:
                    print('Yes')
                else:
                    print(dataset[c][:])                                
                    print(za[a][:])
    za.visitvalues(print_visitor)

