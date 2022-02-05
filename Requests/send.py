""" Simple sending POST request example"""
import requests

URL = "http://127.0.0.1:8000/file"
files = {"my_file": open("README.md", "rb")}
res = requests.post(URL, files=files)
print(res)
print(res.json())
