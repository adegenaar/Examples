[CmdletBinding()]
param(
    [Parameter(Mandatory = $True)]
    [string] 
    $folder,
    
    [Parameter(ValueFromRemainingArguments = $true)] 
    [string[]] 
    $modules
)

# Create the folder if doesn't exist yet
If (!(test-path -Path $folder)) {
    New-Item -ItemType Directory -Path $folder
}

Set-Location -Path $folder

if (test-path -Path requirements.txt ) {
    Remove-Item -Path requirements.txt 
}

foreach ($module in $modules) {
    "$module" | Out-File -filepath .\requirements.txt -Append  
}

if (Test-Path -Path  ".venv") {
    & "C:\Windows\py.exe" -m venv --upgrade .venv
}
else {
    & 'C:\Windows\py.exe' -m venv .venv
}
     
& ".\.venv\scripts\activate.ps1"
& 'C:\Windows\py.exe' -m pip install --upgrade pip
& 'pip' install wheel setuptools black pytest pylint 
& 'pip' install -r requirements.txt
