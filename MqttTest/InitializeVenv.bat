@echo off
python -m venv .venv 
.venv\scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install flake8 pytest
pip install -r requirements.txt
