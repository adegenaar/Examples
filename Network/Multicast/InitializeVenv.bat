@echo off
if exist .venv (
    py -m venv --upgrade .venv  
) else (
    py -m venv .venv 
)
.venv\scripts\activate.bat
py -m pip install --upgrade pip
pip install setuptools wheel black pytest pylint
pip install -r requirements.txt
