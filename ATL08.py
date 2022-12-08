import kerchunk.hdf
import fsspec
import time
import ujson

so = dict(anon=True, default_fill_cache=False, default_cache_type='first')
f = './data/ATL08_20181014084920_02400109_003_01.h5'
fs2 = fsspec.filesystem('')  #local file system to save final jsons to

with fsspec.open(f, **so) as inf:
     start = time.time()
     h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, f, inline_threshold=100)
     end = time.time()
     outf = 'ATL08.json'
     with fs2.open(outf, 'wb') as f:
         f.write(ujson.dumps(h5chunks.translate()).encode());     
     print(end - start)
