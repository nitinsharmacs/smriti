from ..util import generate_uuid, generate_uuids
from ..models.transaction import Transaction


class TxnRepo:
    def __init__(self) -> None:
        self.db: dict[str, Transaction] = {}

    async def get_txn(self, txn_id: str) -> Transaction:
        return self.db[txn_id]

    async def create_new_txn(self, mediaCount: int) -> Transaction:
        txn_id = generate_uuid()
        mediaIds = generate_uuids(mediaCount)

        txn = Transaction(id=txn_id, mediaIds=mediaIds)

        self.db[txn_id] = txn

        return txn

    async def add_media(self, txn_id: str, media_id: str, media_file_path: str):
        txn = self.db[txn_id]
        txn.add_media(media_id, media_file_path)
