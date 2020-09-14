from ext.pickler import Pickler as Pcl
import json

regions = Pcl.get_pickle_file('Cache/files/regions.pickle')
locality = Pcl.get_pickle_file('Cache/files/locality.pickle')
with open('Cache/files/categories.json') as f:
    category = {int(k): int(v) for k, v in json.load(f).items()}
cords: dict = Pcl.get_pickle_file('Cache/files/coords.pickle')

index: dict = Pcl.get_pickle_file('Cache/files/index_cache.p')

index_filename = 'Cache/files/index_cache.p'
vacs_filename = 'Cache/files/struct_actual_vac.pickle'
