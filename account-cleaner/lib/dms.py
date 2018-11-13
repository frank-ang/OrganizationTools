from pprint import pprint
import time

def dms_main(region_name, session, delete=False):
    '''main function called by nuke'''

    dms = session.client('dms', region_name=region_name);

    tasks = dms.describe_replication_tasks()['ReplicationTasks'];
    for task in tasks:
    	ReplicationTaskArn = task['ReplicationTaskArn']
    	print("Found Replication Task: %s" % ReplicationTaskArn)
    	if delete:
    		print("Deleting Replication Task: %s" % ReplicationTaskArn)
    		response = dms.delete_replication_task(ReplicationTaskArn=ReplicationTaskArn)

    replication_instances = dms.describe_replication_instances()['ReplicationInstances'];    
    for instance in replication_instances:
    	ReplicationInstanceArn = instance['ReplicationInstanceArn']
    	print("Found Replication Instance: %s" % ReplicationInstanceArn)
    	if delete:
    		print("Deleting Replication Instance: %s" % ReplicationInstanceArn)
    		response = dms.delete_replication_instance(ReplicationInstanceArn=ReplicationInstanceArn)

    endpoints = dms.describe_endpoints()['Endpoints']
    for endpoint in endpoints: 
    	EndpointArn = endpoint['EndpointArn']
    	print("Found Endpoint: %s" % EndpointArn)
    	if delete:
    		print ("Deleting Endpoint: %s" % EndpointArn)
    		response = dms.delete_endpoint(EndpointArn=EndpointArn)

    subnet_groups = dms.describe_replication_subnet_groups()['ReplicationSubnetGroups']
    for subnet_group in subnet_groups:
    	ReplicationSubnetGroupIdentifier = subnet_group['ReplicationSubnetGroupIdentifier']
    	print("Found ReplicationSubnetGroupIdentifier: %s" % ReplicationSubnetGroupIdentifier)
    	if delete:
    		print ("Deleting ReplicationSubnetGroupIdentifier: %s" % ReplicationSubnetGroupIdentifier)
    		response = dms.delete_replication_subnet_group(ReplicationSubnetGroupIdentifier=ReplicationSubnetGroupIdentifier)
