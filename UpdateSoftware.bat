rem Upgrade Python packages
py -m pip install --upgrade pip
 
pwsh -command "& {py -m pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade-strategy eager --upgrade $_} }"

rem
choco upgrade all -y

rem Upgrade PowerShell Core
pwsh -command "& { Set-PSRepository -Name "PSGallery" -InstallationPolicy Trusted; }"
pwsh -command "& { update-module -AcceptLicense -Force;}"


rem Upgrade PowerShell 5.1
powershell -command "& { update-module -AcceptLicense -Force;}"