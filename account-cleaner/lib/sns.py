from __future__ import print_function
import boto3

def sns_main(region_name, session, delete=False):

    sns_client = session.client('sns', region_name=region_name);
    topics = sns_client.list_topics()['Topics'];
    for topic in topics:
        topic_arn = topic['TopicArn']
        print("Found Topic: %s" % topic_arn)
        if delete:
            print("Deleting Topic: %s" % topic_arn)
            response = sns_client.delete_topic(TopicArn=topic_arn)

