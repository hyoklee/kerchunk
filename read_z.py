import zarr
z = zarr.open('ATL08.zarr')
print(z.tree())
print(z.info)
print(z.attrs)



