from src.smriti.upload.models.transaction import Transaction


def test_should_add_media():
    txn = Transaction(id="txn_id")
    txn.add_media("media1", "/media/path")

    assert txn.mediaIds == ["media1"]
    assert txn.file_paths == ["/media/path"]
