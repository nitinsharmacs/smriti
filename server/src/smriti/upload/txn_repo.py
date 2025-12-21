from .util import generate_uuid, generate_uuids
from .schemas import Transaction


class TxnRepo:
    def __init__(self) -> None:
        self.db = []

    async def create_new_txn(self, mediaCount: int) -> Transaction:
        txnId = generate_uuid()
        mediaIds = generate_uuids(mediaCount)

        txn = Transaction(id=txnId, mediaIds=mediaIds)
        self.db.append(txn)

        return txn

    