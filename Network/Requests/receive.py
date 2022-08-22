""" Simple example for receiving a file """
from typing import Any, Dict, List
from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()


@app.post("/")
async def handle(request: List | Dict | Any = None):
    """handle a request"""
    print(request)
    return request


@app.post("/file")
def _file_upload(my_file: UploadFile = File(...)):
    print(my_file)


if __name__ == "__main__":
    uvicorn.run("receive:app", host="0.0.0.0", port=8000, log_level="debug")
