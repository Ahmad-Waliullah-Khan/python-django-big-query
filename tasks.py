from invoke import Collection
from adtask.ad.tasks import pause_ad_task, unpause_ad_task, update_ad_task
namespace = Collection() 

# Register property tasks
from property.tasks import import_csv
property = Collection('property')
property.add_task(import_csv, name='import')
namespace.add_collection(property)

# Register ad tasks
from ad.tasks import insert_data, calculate_matrix
ad = Collection('ad')
ad.add_task(insert_data, name='insert')
ad.add_task(calculate_matrix, name='calculate')
ad.add_task(pause_ad_task, name='pause')
ad.add_task(unpause_ad_task, name='unpause')
ad.add_task(update_ad_task, name='update')
namespace.add_collection(ad)

