from __future__ import print_function
import boto3

def apigateway_main(region_name, session, delete=False):

    apigateway_client = session.client('apigateway', region_name=region_name);
    
    rest_api_list = apigateway_client.get_rest_apis()['items'];
    for rest_api in rest_api_list:
        rest_api_id = rest_api['id']
        print("Found REST API %s / %s" % (rest_api['id'], rest_api['name']))
        if delete:
            print("Deleting REST API %s / %s" % (rest_api['id'], rest_api['name']))
            apigateway_client.delete_rest_api(restApiId=rest_api_id)

    api_key_list = apigateway_client.get_api_keys()['items'];
    for api_key in api_key_list:
        api_key_id = api_key['id']
        print("Found API Key: %s" % api_key_id)
        if delete:
            print("Deleting API Key ID: %s" % api_key_id)
            apigateway_client.delete_api_key(apiKey=api_key_id)

