from fastapi import APIRouter, File, Form, UploadFile

from .repo.media_repo import MediaRepo

from .repo.store import FileStore, Store

from .repo.txn_repo import TxnRepo

from .schemas import (
    CommitTxnReq,
    CommitTxnRes,
    NewTxnReqBody,
    NewTxnRes,
    UploadRes,
)
from .service import UploadService


def create_router():
    uploadService = UploadService(TxnRepo(), Store(FileStore()), MediaRepo())

    upload_router = APIRouter(prefix="/upload")

    @upload_router.post("/create-txn")
    async def create_upload_txn(txn_req: NewTxnReqBody):
        txn = await uploadService.create_txn(txn_req.mediaCount)

        return NewTxnRes(status=201, txnId=txn.id, mediaIds=txn.mediaIds)

    @upload_router.post("/upload")
    async def upload(
        txnId: str = Form(),
        mediaId: str = Form(),
        file: UploadFile = File(),
    ):
        filepath = await uploadService.upload_file(txnId, mediaId, file)
        return UploadRes(status=201, filepath=filepath)

    @upload_router.put("/commit")
    async def commit_upload_txn(txn: CommitTxnReq):
        await uploadService.commit_txn(txn.txn_id)
        return CommitTxnRes(status=201, txn_id=txn.txn_id)

    return upload_router
