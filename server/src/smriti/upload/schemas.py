from pydantic import BaseModel


class Response(BaseModel):
    status: int


class NewTxnReqBody(BaseModel):
    mediaCount: int


class NewTxnRes(Response):
    txnId: str
    mediaIds: list[str]


class UploadRes(Response):
    filepath: str


class CommitTxnReq(BaseModel):
    txn_id: str


class CommitTxnRes(Response):
    txn_id: str
