from fastapi import APIRouter

from .txn_repo import TxnRepo

from .schemas import NewTxnReqBody, NewTxnRes
from .service import UploadService


def create_router():
    uploadService = UploadService(TxnRepo())

    upload_router = APIRouter(prefix="/upload")

    @upload_router.post("/create-txn")

    async def create_upload_txn(txn_req: NewTxnReqBody):
        txn = await uploadService.create_txn(txn_req.mediaCount)

        return NewTxnRes(status=200, txnId=txn.id, mediaIds=txn.mediaIds)

    return upload_router
