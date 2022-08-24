from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os
import sys
import time
import threading

ComputeEngine = get_driver(Provider.GCE)
driver2 = ComputeEngine('617425714923-compute@developer.gserviceaccount.com', '/home/pi/key.json', project='tese-de-mestrado')
driver = ComputeEngine('869453422007-compute@developer.gserviceaccount.com', '/home/pi/key2.json', project='tese-de-mestrado-343711')
nodes = driver2.list_nodes(ex_zone=None, ex_use_disk_cache=False)

command = str(sys.argv[1])

def func(n):
	if n.name == 'ipfs-bootstrap' or n.name == 'ipfs-db-server' or n.name == 'test-instance':
		pass
	else:
		sshCommand = "ssh -o StrictHostKeyChecking=no -i /home/pi/.ssh/mestrado matiasfrazaocorreia@" + n.public_ips[0] + " 'bash -s' < " + command
		while os.system(sshCommand):
			time.sleep(1)


if __name__ == "__main__":
	threads = list()
	number = 0
	for node in nodes:
		print("Main    : create and start thread %d.", number)
		number = number + 1
		x = threading.Thread(target=func, args=(node,))
		threads.append(x)
		x.start()
	for index, thread in enumerate(threads):
		print("Main    : before joining thread %d.", index)
		thread.join()
		print("Main    : thread %d done", index)
