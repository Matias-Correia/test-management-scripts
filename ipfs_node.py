from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.types import NodeState
import random
import sys
import os
import time
import threading

ComputeEngine = get_driver(Provider.GCE)
driver = ComputeEngine('869453422007-compute@developer.gserviceaccount.com', '/home/pi/key2.json', project='tese-de-mestrado-343711')
driver2 = ComputeEngine('617425714923-compute@developer.gserviceaccount.com', '/home/pi/key.json', project='tese-de-mestrado')
zones = driver.ex_list_zones()
number_of_new_nodes = int(sys.argv[1])

def create_nodes(n):
	zone = random.choice(zones)
	name = 'ipfs-node-'+ str(n+1)
	print('Zone: %s' % (zone))
	if str(zone).count('europe') > 0:
		snap = driver2.ex_get_snapshot('export-eu')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('asia') > 0:
		snap = driver2.ex_get_snapshot('export-asia')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('australia') > 0:
		snap = driver2.ex_get_snapshot('export-asia')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('us') > 0:
		snap = driver2.ex_get_snapshot('export-us')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('southamerica') > 0:
		snap = driver2.ex_get_snapshot('export-us')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	elif str(zone).count('northamerica') > 0:
		snap = driver2.ex_get_snapshot('export-us')
		driver2.create_volume(10, name=name, location=zone, snapshot=snap, image=None, use_existing=True, ex_disk_type='pd-standard', ex_image_family=None)
	node = driver2.create_node(name=name, size='e2-small', image=None, location=zone, ex_network='default', ex_subnetwork=None, ex_tags=None, ex_metadata=None, ex_boot_disk=name, use_existing_disk=True, external_ip='ephemeral', internal_ip=None, ex_disk_type='pd-standard', ex_disk_auto_delete=True, ex_service_accounts=None, description=None, ex_can_ip_forward=None, ex_disks_gce_struct=None, ex_nic_gce_struct=None, ex_on_host_maintenance=None, ex_automatic_restart=None, ex_preemptible=None, ex_image_family=None, ex_labels=None, ex_accelerator_type=None, ex_accelerator_count=None, ex_disk_size=None)
	sshCommand = "ssh -o StrictHostKeyChecking=no -i /home/pi/.ssh/mestrado matiasfrazaocorreia@" + node.public_ips[0] + " 'bash -s' < /home/pi/ipfs_configuration_script.sh '" + node.private_ips[0] + "' 1 " + "'34.118.36.194:50051' " + "500"
	while os.system(sshCommand):
		time.sleep(1)

threads = list()
for number in range(number_of_new_nodes):
	print("Main    : create and start thread %d.", number)
	x = threading.Thread(target=create_nodes, args=(number,))
	threads.append(x)
	x.start()

for index, thread in enumerate(threads):
        print("Main    : before joining thread %d.", index)
        thread.join()
        print("Main    : thread %d done", index)
