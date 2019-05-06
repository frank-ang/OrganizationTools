# Powershell script to add a new user.
$name = "newuser"
$password = "CHANGE_ME"
New-ADUser -Name "$name" -GivenName "$name" -Surname "$name" -SamAccountName "$name" `
-UserPrincipalName "$name@corp.demo.com" -Path "OU=Users,OU=CORP,DC=corp,DC=demo,DC=com" `
-AccountPassword(ConvertTo-SecureString -AsPlainText "$password" -Force) -Enabled $true -PasswordNeverExpires $true