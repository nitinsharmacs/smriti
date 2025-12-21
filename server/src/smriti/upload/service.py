from fastapi import UploadFile

from .repo.media_repo import MediaRepo

from .repo.store import Store
from .repo.txn_repo import TxnRepo
from .models.transaction import Transaction


class UploadService:
    def __init__(
        self, txn_repo: TxnRepo, store: Store, media_repo: MediaRepo
    ) -> None:
        self.txn_repo = txn_repo
        self.media_repo = media_repo
        self.store = store

    async def create_txn(self, mediaCount: int) -> Transaction:
        return await self.txn_repo.create_new_txn(mediaCount)

    async def upload_file(
        self, txnId: str, mediaId: str, file: UploadFile
    ) -> str:
        filepath: str = await self.store.save_temporarily(
            file.file, file.filename
        )

        await self.txn_repo.add_media(txnId, mediaId, filepath)

        return filepath

    async def commit_txn(self, txn_id: str):
        txn = await self.txn_repo.get_txn(txn_id)
        new_paths = await self.store.save_permanently(txn.file_paths)
        await self.media_repo.add_new_media(txn.mediaIds, new_paths)
