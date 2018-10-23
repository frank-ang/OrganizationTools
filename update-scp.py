''' Update SCP with the SCP JSON in local directory '''

import argparse
import boto3
import csv
import pdb
import sys
import getpass
import re
from pprint import pprint

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# In python 2.x, input() requires quotes for the input therefore
# replace with raw_input for python 2.x 
try:
    input = raw_input
except NameError:
    pass

const SCP_DIRECTORY_PATH="./scp/"

def update_scp():
    ''' updates SCP policies with what exists in local diretory '''

    session = boto3.session.Session()
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    user_id = boto3.client('sts').get_caller_identity().get('UserId')

    # 1. Scan files in local directory. extract names of SCPs.

    #days_file = open(path,'r')
    for x in os.listdir(SCP_DIRECTORY_PATH):
        print x

    # 2. Find IDs of SCPs

    # 3. Update SCPs

    # Prompt Confirmation
    print ("Syncing SCPs:")
    print ("  AccountId: %s \n  UserId: %s \n other info TODO \n" \
        % (account_id, user_id))
    if not args.force:
        choice = input("Please review options. Proceed? (y/n): ").lower()
        if choice not in ('yes', 'y', 'Y'):
            print("Exiting")
            sys.exit(-1)

    print('-Finished updating SCPs in account: %s' % (account_id))

        
if __name__ == '__main__':

    description = '''Organizations SCP updater.'''

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-r', '--regions',
        action='store',
        help='Specify one or more AWS regions separated by comma,' 
        ' e.g. us-east-1,us-west-2'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        help='Skip interactive prompts for confirmation'
    )
    parser.add_argument(
        '-c', '--create',
        default=False,
        action='store_true',
        help='Creates SCP if does not exist.'
        ' default: %(default)s'
    )
    args = parser.parse_args()

    update_scp()
