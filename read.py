import glob
import xarray as xr

for f in glob.glob("*.h*5.json"):
    print(f)
    backend_args = {"consolidated": False, "storage_options": {"fo": f}}
    ds = xr.open_dataset("reference://", engine="zarr", backend_kwargs=backend_args)
    print(ds)
