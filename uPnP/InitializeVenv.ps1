if (Test-Path -Path  ".venv") {
    & "C:\Windows\py.exe" -m venv --upgrade .venv
}
else {
    & 'C:\Windows\py.exe' -m venv .venv
}
     
& ".\.venv\scripts\activate.ps1"
& 'C:\Windows\py.exe' -m pip install --upgrade pip
& 'pip' install setuptools wheel black pytest pylint
& 'pip' install -r requirements.txt
