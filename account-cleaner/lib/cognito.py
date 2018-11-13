from __future__ import print_function
import boto3

def cognito_main(region_name, session, delete=False):

    cognito_client = session.client('cognito-idp', region_name=region_name);
    user_pool_list = cognito_client.list_user_pools(MaxResults=10)['UserPools']
    for pool in user_pool_list:
        pool_id = pool['Id']
        pool_name = pool['Name']
        print("Pool: %s / %s" % (pool_id,pool_name))
        if delete:
            print("Deleting Pool: %s" % pool_id)
            response = cognito_client.delete_user_pool(UserPoolId=pool_id)

