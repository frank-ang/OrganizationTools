# AWS Nuke examples

1. Edit [./nuke-all.yaml]() file, replacing with your own region and account IDs.

2. Set AWS environment variables to the account being nuked

3. Dry-run nuke.  
  
  ```
aws-nuke --config ./nuke-all.yaml \
--access-key-id $AWS_ACCESS_KEY_ID \
--session-token $AWS_SESSION_TOKEN \
--secret-access-key $AWS_SECRET_ACCESS_KEY

  ```
4. Really nuke. 
   
   Append the parameter: ```--no-dry-run```