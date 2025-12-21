
from .txn_repo import TxnRepo
from .schemas import Transaction


class UploadService():
    def __init__(self, txn_repo: TxnRepo) -> None:
        self.txn_repo = txn_repo
        

    async def create_txn(self, mediaCount: int) -> Transaction:
        return await self.txn_repo.create_new_txn(mediaCount)
