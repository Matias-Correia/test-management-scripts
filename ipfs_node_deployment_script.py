from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import random
import sys

# This example assumes you are running on an instance within Google
# Compute Engine. As such, the only value you need to specify is
# the Project ID. The GCE driver will the consult GCE's internal
# metadata service for an authorization token.
#
# You must still place placeholder empty strings for user_id / key
# due to the nature of the driver's __init__() params.
ComputeEngine = get_driver(Provider.GCE)
driver = ComputeEngine('617425714923-compute@developer.gserviceaccount.com', '/home/pi/key.json', project='tese-de-mestrado')

zones = driver.ex_list_zones()

number_of_new_nodes = int(sys.argv[1])

for n in range(number_of_new_nodes):
	zone = random.choice(zones)
	name = 'IPFS_Node_'+ str(n)
	print('Zone: %s' % (zone))
	if str(zone).count('europe') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('asia') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode-asia', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('australia') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode-asia', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('us') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode-us', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('southamerica') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode-us', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('northamerica') > 0:
		driver.create_volume(10, name=name, location=zone, snapshot='ipfsnode-us', image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
