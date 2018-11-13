from pprint import pprint
import time

def cloudformation_main(region_name, session, delete=False):
    '''main function called by nuke'''

    client = session.client('cloudformation', region_name=region_name);

    stack_sets = client.list_stack_sets()['Summaries'];
    for stack_set in stack_sets:
    	StackSetName = stack_sets['StackSetName']
    	print("Found StackSetName: %s" % StackSetName)
    	if delete:
    		print("Deleting StackSetName : %s" % StackSetName)
    		response = client.delete_stack_set(StackSetName=StackSetName)

    stacks = client.list_stacks()["StackSummaries"]
    for stack in stacks:
        StackName = stack["StackName"]
        print("Found Stack: %s" % StackName)
        if delete:
            print("Deleting StackName : %s" % StackName)
            response = client.delete_stack(StackName=StackName)        