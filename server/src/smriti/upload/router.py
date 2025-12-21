from fastapi import APIRouter, File, Form, UploadFile

from .store import FileStore, Store

from .txn_repo import TxnRepo

from .schemas import NewTxnReqBody, NewTxnRes, UploadRes
from .service import UploadService


def create_router():
    uploadService = UploadService(TxnRepo(), Store(FileStore()))

    upload_router = APIRouter(prefix="/upload")

    @upload_router.post("/create-txn")
    async def create_upload_txn(txn_req: NewTxnReqBody):
        txn = await uploadService.create_txn(txn_req.mediaCount)

        return NewTxnRes(status=200, txnId=txn.id, mediaIds=txn.mediaIds)

    @upload_router.post("/upload")
    async def upload(
        txnId: str = Form(),
        mediaId: str = Form(),
        file: UploadFile = File(),
    ):
        filepath = await uploadService.upload_file(txnId, mediaId, file)
        return UploadRes(status=201, filepath=filepath)

    return upload_router
