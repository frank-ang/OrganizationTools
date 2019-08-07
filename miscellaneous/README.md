# Miscellaneous

## Setup CloudTrail for Organizations 

See docs.

## Setup Predefined CloudWatch Alarms

Setup [CloudFormation template with predefined CloudWatch metric filters and alarms]
(https://docs.aws.amazon.com/awscloudtrail/latest/userguide/use-cloudformation-template-to-create-cloudwatch-alarms.html)


### Searching CloudWatch Logs Insights (from CloudTrail)

The CloudFormation stack creates several CloudWatch logs filters, on patterns like:
```
{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }
```

If you receive a number of "CloudTrailAuthorizationFailures" emails, dive into the root causes why this is happening. 

E.g. Find errorCode="AccessDenied"

```
fields @timestamp, errorCode, @message
| sort @timestamp desc 
| filter errorCode like /(?i)accessdenied/
| limit 25
```

Notes:
* turn on case insensitive: ```(?i)```.

e.g. if the auth errors appear to be generally associated with S3 bucket resources. Identify the buckets and callers.
```
fields @timestamp, sourceIPAddress, errorCode, eventName, resources.1.ARN, userIdentity.invokedBy
| filter errorCode like /(?i)denied/
| sort @timestamp desc 
| limit 1000
```

We see config.amazonaws.com, s3.amazonaws.com, securityhub.amazonaws.com, etc. these are regular compliance checks.

## Searching CloudTrail events using CLI

E.g. Dump all events from a specific time.
```
aws cloudtrail lookup-events --start-time '2019-08-07, 03:00'
```

E.g. search for cause of AuthorizationFailureCount


## Setup CloudTrail logging to Athena

TODO: Update, test, and fix inaccuracies.


### Example: Manually re-partition CW Logs into Athena. 

```
ALTER TABLE cloudtrail_logs ADD PARTITION (account='REPLACE_ACCOUNT_ID', region='us-east-1', year='2018') location 's3://mycloudtrail01/AWSLogs/REPLACE_ACCOUNT_ID/CloudTrail/us-east-1/2018/'
```

### Work-in-progress Automate re-partitioning with Lambda.

TODO work in progress.

Lambda IAM policy, I suppose.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": [
                "arn:aws:s3:::aws-athena-query-results-109826131385-us-east-1",
                "arn:aws:s3:::mycloudtrail01"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::aws-athena-query-results-109826131385-us-east-1/*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:GetObjectTagging",
                "s3:GetBucketPolicy"
            ],
            "Resource": [
                "arn:aws:s3:::mycloudtrail01",
                "arn:aws:s3:::mycloudtrail01/*"
            ]
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "athena:StartQueryExecution",
                "athena:CreateNamedQuery",
                "athena:RunQuery"
            ],
            "Resource": "*"
        }
    ]
}
```


