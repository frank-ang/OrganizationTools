# Cleanup sandbox accounts

> ## Prerequisites

> 1. Give each sandbox account an alias name.

>    * Set ```AWS*``` session credentials for "sandboxNN", then execute: 
> ```
> create-account-alias --account-alias "sandboxNN"
> ```
>      Reference: [IAM Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html#CreateAccountAlias)

> 1. Install AWS Nuke
  

## AWS Nuke usage

1. Edit [./nuke-all.yaml]() file, replacing with your own region and account IDs.

2. Set AWS* environment variables to the account being nuked

3. Dry-run nuke.  
  
  ```
aws-nuke --config ./nuke-all.yaml \
--access-key-id $AWS_ACCESS_KEY_ID \
--session-token $AWS_SESSION_TOKEN \
--secret-access-key $AWS_SECRET_ACCESS_KEY

  ```
4. Really nuke. 
   
   Append the parameter: ```--no-dry-run```


For more info, refer to [https://github.com/rebuy-de/aws-nuke](https://github.com/rebuy-de/aws-nuke)
