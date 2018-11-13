'''module to Nuke the contents of S3'''
from __future__ import print_function
import boto3

def s3_main(region_name, session, delete=False):
    s3_resources = session.resource('s3',
        region_name=region_name
    )

    s3_client = s3_resources.meta.client
    for bucket in s3_resources.buckets.all():
        location = s3_client.get_bucket_location(Bucket=bucket.name)['LocationConstraint']
        if (location == region_name or (not location and region_name == 'us-east-1')):
            print("Remove S3 bucket: " + bucket.name, end=' ')
            if delete:
                print("\tDeleting S3 objects...", end=' ')
                #Add in exception handling.  If a bucket is deleted 
                #it may still exist on an ls for up to 24 hours
                try:
                    bucket.objects.all().delete()
                    bucket.object_versions.all().delete()
                    bucket.delete()
                    print(" \t[Done]")
                except:
                    print("\n***Error occurred on bucket", bucket.name, "in region", region_name, ".\n***Ignoring and continuing.")
            else:
                print()
        
