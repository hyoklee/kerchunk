import kerchunk.hdf
import fsspec

so = dict(anon=True, default_fill_cache=False, default_cache_type='first')
singles = []
f = 'data/ATL08_20181014084920_02400109_003_01.h5'
with fsspec.open(f, **so) as inf:
     h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, u, inline_threshold=100)
     singles.append(h5chunks.translate())

