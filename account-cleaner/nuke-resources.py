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


from lib.autoscaling import autoscaling_main
from lib.sns import sns_main
from lib.apigateway import apigateway_main
from lib.cognito import cognito_main
from lib.dms import dms_main
from lib.glue import glue_main
from lib.cloudformation import cloudformation_main
from lib.s3 import s3_main
from lib.iam import iam_main


all_regions = [ 'us-east-1' ]

supported_services = {
    'iam': True,
    'ec2': False,
    'rds': False,
    's3' : True,
    'vpc': False,
    'dms': True,
    'glue': True,
    'cloudformation': True,
}

# In python 2.x, input() requires quotes for the input therefore
# replace with raw_input for python 2.x 
try:
    input = raw_input
except NameError:
    pass

def main(specified_regions, clean_services):
    ''' wrapper function calling service specific account cleaners '''

    session = boto3.session.Session()
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    user_id = boto3.client('sts').get_caller_identity().get('UserId')

    # Confirm
    print ("Resource Nuke options:")
    print ("  AccountId: %s \n  UserId: %s \n  Services: %s \n  Regions: %s" \
        % (account_id, user_id, str(clean_services), str(specified_regions)))
    if not args.force:
        choice = input("Please review options. Proceed? (y/n): ").lower()
        if choice not in ('yes', 'y', 'Y'):
            print("Exiting")
            sys.exit(-1)

    for region in specified_regions:
        if 'all' in clean_services or 'cognito' in clean_services:
            print("-Starting Cognito purge for Account: %s, Regions: %s" % (account_id, region))
            cognito_main(region, session, delete=args.delete);
        if 'all' in clean_services or 'apigateway' in clean_services:
            print("-Starting API Gateway purge for Account: %s, Regions: %s" % (account_id, region))
            apigateway_main(region, session, delete=args.delete);
        if 'all' in clean_services or 'asg' in clean_services:
            print("-Starting AutoScaling purge for Account: %s, Regions: %s" % (account_id, region))
            autoscaling_main(region, session, delete=args.delete);
        if 'all' in clean_services or 'sns' in clean_services:
            print("-Starting SNS purge for Account: %s, Regions: %s" % (account_id, region))
            sns_main(region, session, delete=args.delete);
        if 'all' in clean_services or 'dms' in clean_services:
            print("-Starting DMS purge for Account: %s, Regions: %s" % (account_id, region))
            dms_main(region, session, delete=args.delete);
        if 'all' in clean_services or 'glue' in clean_services:
            print("-Starting Glue purge for Account: %s, Regions: %s" % (account_id, region))
            glue_main(region, session, delete=args.delete);    
        if 'all' in clean_services or 's3' in clean_services:
            print("-Starting S3 purge for Account: %s, Regions: %s" % (account_id, region))
            s3_main(region, session, delete=args.delete);    
        if 'all' in clean_services or 'cloudformation' in clean_services:
            print("-Starting CloudFormation purge for Account: %s, Regions: %s" % (account_id, region))
            cloudformation_main(region, session, delete=args.delete);    

    if 'all' in clean_services or 'iam' in clean_services:
        # print("\n-SKIPPING IAM purge for Account: %s" % (account_id))
        access_key = os.environ['AWS_ACCESS_KEY_ID']
        iam_main(access_key, session, delete=args.delete);
    
    print('-Finished processing account: %s, regions: %s' % (account_id, specified_regions))


def check_service_region(session, region, service):
    if (region in session.get_available_regions(service)):
        return True
    else:
        return False
        
if __name__ == '__main__':

    description = '''Account Cleaner.'''

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
        '-s', '--services',
        action='store',
        help='Specify one or more AWS services you want to cleanup,' 
        " e.g. iam,ec2\n"
        'By default will try for all the services supported by this script'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        help='Skip interactive prompts for confirmation'
    )
    parser.add_argument(
        '-d', '--delete',
        default=False,
        action='store_true',
        help='Deletes resources. No Dry-run'
        ' default: %(default)s'
    )
    args = parser.parse_args()

    region_names = None
    
    # check to ensure environment variables are set.
    if 'AWS_SESSION_TOKEN' not in os.environ \
        or 'AWS_SECRET_ACCESS_KEY' not in os.environ \
        or 'AWS_ACCESS_KEY_ID' not in os.environ:
            print("Please ensure your AWS Environment Variables are set to the account creds you require.")
            sys.exit(0)

    if args.regions:
        region_names = [x.strip() for x in args.regions.split(',')]
        for rname in region_names:
            match = re.search(r"\w+-\w+-\d+$", rname)
            if not match:
                sys.exit("Error: %s doesn't look like a region name." % rname)

    clean_services = {}
    if args.services:
        services_names = [x.strip().lower() for x in args.services.split(',')]
        for sname in services_names:
            if sname == 'all':
                clean_services['all'] = True
                break;
            if sname in supported_services:
                clean_services[sname.lower()] = True
            else:
                sys.exit("Error: service %s is not currently supported." % sname)
    else:
        clean_services['all'] = True

    session = boto3.session.Session()
       
    specified_regions = list()
    if region_names:
        name_region = [] 

        for rname in region_names:
            if rname in all_regions:
                specified_regions.append(rname)
            else:
                sys.exit("Error: cannot find region %s." % rname)

    if specified_regions:
        main(specified_regions, clean_services)
    else:
        main(all_regions, clean_services)