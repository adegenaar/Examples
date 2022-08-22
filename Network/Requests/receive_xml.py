""" simple receive xml via FatAPI example"""
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from typing import Any, Generic, Type, TypeVar
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, FastAPI, File, UploadFile
import simplexml
from starlette.requests import Request
from starlette.responses import Response
import uvicorn

T = TypeVar("T", bound=BaseModel)

router = APIRouter()


class Item(BaseModel):
    """Pydantic dataclass"""

    name: str = None
    price: float = None
    is_offer: bool = None


class XmlResponse(Response):
    """XML version of the response class"""

    media_type = "text/xml"

    def render(self, content: Any) -> bytes:
        return simplexml.dumps({"response": content}).encode("utf-8")


class XmlBody(Generic[T]):
    """New type for the XML Body"""

    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    async def __call__(self, request: Request) -> T:
        """the following check is unnecessary if always using xml,
        but enables the use of json too"""
        if request.headers.get("Content-Type") == "application/xml":
            body = await request.body()
            dict_data = simplexml.loads(body)
        else:
            dict_data = await request.json()
        return self.model_class.parse_obj(dict_data["Item"])


app = FastAPI()


@app.post("/xml")
async def process_item(item: Item = Depends(XmlBody(Item)), header: str = Header(None)):
    """accept xml in the body"""
    print(item)
    print(header)
    # process a single item
    return XmlResponse({"person": {"name": "joaquim", "age": 15, "cars": [{"id": 1}, {"id": 2}]}})


@app.post("/file")
def _file_upload(my_file: UploadFile = File(...)):
    print(my_file)


if __name__ == "__main__":
    uvicorn.run("receive_xml:app", host="0.0.0.0", port=8000, log_level="debug")
