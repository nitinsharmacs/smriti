from typing import BinaryIO
from pydantic import BaseModel

class Response(BaseModel):
    status: int

class NewTxnReqBody(BaseModel):
    mediaCount: int

class NewTxnRes(Response):
    status: int
    txnId: str
    mediaIds: list[str]


class UploadRes(Response):
    filepath: str


class Transaction(BaseModel):
    id: str
    mediaIds: list[str] = []
    file_paths: list[str] = []


