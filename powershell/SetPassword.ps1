# Resets passwords for multiple users. 
# User names are appended with an index, e.g. "user01"
$StartUserIndex=1
$EndUserIndex=20
$UserNamePrefix="user"

[Reflection.Assembly]::LoadWithPartialName("System.Web")
[Reflection.Assembly]::LoadWithPartialName("Regex")

function SetPassword ($name,$password) {
   Set-ADAccountPassword -Identity "$name" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "$password" -Force)  
   echo "user: $name , password: $password"
}

function ResetPasswords() {
    For ($i=$StartUserIndex; $i -le $EndUserIndex; $i++) {
         $randomStr = [System.Web.Security.Membership]::GeneratePassword(6,0)
         $randomStr = $randomStr -replace '[^a-zA-Z0-9]', (Get-Random -Minimum 0 -Maximum 10).ToString()
         $prefix = "Cod3." # to meet AD upper/lower/num/symbol complexity policy.
         $password = $prefix + $randomStr

         $name = "$UserNamePrefix" + "$i".Padleft(2,'0')
         Try {
              SetPassword $name $password
         } Catch [Exception] {
              echo $_.Exception.GetType().FullName, $_.Exception.Message
         }
    }
}

ResetPasswords
