from pydantic import BaseModel


class NewTxnReqBody(BaseModel):
    mediaCount: int

class NewTxnRes(BaseModel):
    status: int
    txnId: str
    mediaIds: list[str]



class Transaction(BaseModel):
    id: str
    mediaIds: list[str] = []
    file_paths: list[str] = []