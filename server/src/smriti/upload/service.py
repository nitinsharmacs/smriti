from fastapi import UploadFile

from .store import Store
from .txn_repo import TxnRepo
from .schemas import Transaction


class UploadService:
    def __init__(self, txn_repo: TxnRepo, store: Store) -> None:
        self.txn_repo = txn_repo
        self.store = store

    async def create_txn(self, mediaCount: int) -> Transaction:
        return await self.txn_repo.create_new_txn(mediaCount)

    async def upload_file(
        self, txnId: str, mediaId: str, file: UploadFile
    ) -> str:
        filepath: str = await self.store.save_temporarily(
            file.file, file.filename
        )

        # await self.txn_repo.add_media(txnId, mediaId, filepath)

        return filepath
