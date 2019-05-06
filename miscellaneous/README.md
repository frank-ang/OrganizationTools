# My Organization central logging account.

## Example: re-partition CW Logs into Athena. 
ALTER TABLE cloudtrail_logs ADD PARTITION (account='331780945983', region='us-east-1', year='2018') location 's3://mycloudtrail01/AWSLogs/331780945983/CloudTrail/us-east-1/2018/'

## 2. How to automate.
Lambda.

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
