@echo off
if exist .venv (
    python -m venv --upgrade .venv  
) else (
    python -m venv .venv 
)
.venv\scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install black pytest
pip install -r requirements.txt
