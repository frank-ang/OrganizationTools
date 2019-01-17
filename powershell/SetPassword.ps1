$StartUserIndex=1
$EndUserIndex=20

[Reflection.Assembly]::LoadWithPartialName("System.Web")
[Reflection.Assembly]::LoadWithPartialName("Regex")

function SetPassword ($name,$password) {
   Set-ADAccountPassword -Identity "$name" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "$password" -Force)  
   echo "user: $name , password: $password"
}

For ($i=$StartUserIndex; $i -le $EndUserIndex; $i++) {    
     $randomStr = [System.Web.Security.Membership]::GeneratePassword(6,0)
     $randomStr = $randomStr -replace '[^a-zA-Z0-9]', (Get-Random -Minimum 0 -Maximum 10).ToString()
     $prefix = "Cod3." # to meet AD upper/lower/num/symbol complexity policy.
     $password = $prefix + $randomStr

     $name = "user" + "$i".Padleft(2,'0')
     Try {
          SetPassword $name $password
     } Catch [Exception] {
          # retry 1x
          echo "Retrying..."
          SetPassword $name $password
     }
}
