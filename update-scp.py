''' 
Synchonizes SCP by uploading latest SCP JSON from the local directory.

'''

import argparse
import boto3
import glob
import csv
import pdb
import sys
import getpass
import re
import json
from pprint import pprint

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# In python 2.x, input() requires quotes for the input therefore
# replace with raw_input for python 2.x 
try:
    input = raw_input
except NameError:
    pass

SCP_DIRECTORY_PATH = "./scp/"

def update_scp():
    ''' updates SCP policies with what exists in local diretory '''

    session = boto3.session.Session()
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    user_id = boto3.client('sts').get_caller_identity().get('UserId')

    scp_dict = dict()
    # 1. SCP files are in local directory. SCP names based on JSON filename.
    for filename in glob.glob(SCP_DIRECTORY_PATH + "*.json"):
        basename = os.path.splitext(os.path.basename(filename))[0]
        print "Local SCP File: %s" % filename
        scp_dict[basename] = { "filename": filename } 

    ### print (scp_dict)
    # 2. Find IDs of SCPs

    org_client = boto3.client("organizations")

    print "Finding exisitng active SCP that match..."
    # print(org_client.list_policies(Filter='SERVICE_CONTROL_POLICY')["Policies"])
    active_policies = org_client.list_policies(Filter='SERVICE_CONTROL_POLICY')["Policies"]
    for active_policy in active_policies:
        policy_name = active_policy["Name"]
        # Find matching local SCP file 
        if (policy_name in scp_dict):
            # matching local SCP file. Compare diff and flag for update.
            scp_dict[policy_name]["id"] = active_policy["Id"]

            local_policy_content = open(scp_dict[policy_name]['filename'], 'r').read()
            local_json = json.dumps(local_policy_content, sort_keys=True)

            active_policy = org_client.describe_policy(PolicyId=active_policy["Id"])
            active_policy_content = active_policy["Policy"]["Content"]
            active_json = json.dumps(active_policy_content, sort_keys=True)

            if (local_json != active_json):
                scp_dict[policy_name].update( { "status": False })
                print("Local Policy and active Policy content differs for: " + policy_name)

        else:
            # no matching local SCP file. Skip.
            continue


    # Prompt Confirmation
    print ("Summary:")
    print ("  AccountId: %s \n  UserId: %s \n" % (account_id, user_id))
    count_scps_to_sync = 0;
    for name,scp in scp_dict.items():
        if "status" in scp and scp["status"] == False:
            count_scps_to_sync += 1
            print "Updating SCP name/id/filename: %s / %s / %s" % (name, scp["id"], scp["filename"])
    print ("SCPs that need to be updated: %d" % count_scps_to_sync)

    if count_scps_to_sync < 1:
        sys.exit(0)

    if not args.force:
        choice = input("Please review options. Proceed? (y/n): ").lower()
        if choice not in ('yes', 'y', 'Y'):
            print("Exiting")
            sys.exit(-1)

    for name,scp in scp_dict.items():
        if "status" in scp and scp["status"] == False:
            print "SCP to be updated (name/id/filename): %s / %s / %s" % (name, scp["id"], scp["filename"])
            local_policy_content = open(scp['filename'], 'r').read()
            response = org_client.update_policy(
                PolicyId=scp["id"],
                Content=local_policy_content
            )

    print('-Finished updating SCPs in account: %s' % (account_id))

        
if __name__ == '__main__':

    description = '''Organizations SCP updater.'''

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        help='Skip interactive prompts for confirmation'
    )
    args = parser.parse_args()

    update_scp()
