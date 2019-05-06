# AWS Multi Account Setup 

Scripts to enable management of a multi-account envioronment. 
The main purpose of these tools are to manage student accounts for workshops.

## Design

![Multi-account architecture](doc/MultiAccount.jpg) 

## Scripts

### PowerShell scripts for Active Directory user management.

**[./powershell/SetPassword.ps1](./powershell/SetPassword.ps1)**: Resets Active Directory user passwords. Run from the AD Tools Windows Server.

### Sample Service control policies (SCP) for AWS Organizations.

**[./scp/](./scp/)**: directory containing sample SCP json files to be atteched to the sandbox OU.

### Sample Permissions Policies for AWS Single Sign-on. 

**[./sso/](./sso/)**: directory containing AWS SSO Permissions Policies, requires copy-paste into the SSO console manually, since the SSO API is currently not available. 

## Clean up sandboxes with aws-nuke

After a workshop, reset credentials, then cleanup sandbox accounts to prepare them for reuse. 

See [https://github.com/rebuy-de/aws-nuke](https://github.com/rebuy-de/aws-nuke)
After installation, quick instructions, see: [./aws-nuke-config/](./aws-nuke-config/)



