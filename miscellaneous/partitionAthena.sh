#!/bin/bash
echo "Loading athena partitions..."

# --- Replace the following. ---
BUCKET="mycloudtrail01"
ATHENA_OUTPUT_LOCATION="s3://aws-athena-query-results-109826131385-us-east-1"
PARENT_ORG_ID="ou-80lg-bg3qmuah"
YEAR="2018"
# --- ---

ACCOUNTS_ARRAY=`aws organizations list-accounts-for-parent --parent-id "$PARENT_ORG_ID" --output text | cut -f4`
REGIONS_ARRAY=`aws ec2 describe-regions --output text | cut -f3`

for ACCOUNT in $ACCOUNTS_ARRAY
do
	for REGION in $REGIONS_ARRAY
	do
		for MONTH in `seq -w 01 12`
		do
		    echo -e "Adding partition to account: '$ACCOUNT', region:'$REGION', year,month:'$YEAR','$MONTH' ..."
			QUERY="ALTER TABLE cloudtrail_logs ADD PARTITION (account='$ACCOUNT', region='$REGION', year='$YEAR', month='$MONTH') location 's3://$BUCKET/AWSLogs/$ACCOUNT/CloudTrail/$REGION/$YEAR/$MONTH/'"
			echo "Executing Query: $QUERY" 
			aws --region us-east-1 athena start-query-execution --query-string "$QUERY" --result-configuration "OutputLocation=$ATHENA_OUTPUT_LOCATION"
		done
	done
done
