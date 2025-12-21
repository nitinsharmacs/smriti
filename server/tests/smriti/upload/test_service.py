from unittest.mock import AsyncMock, Mock
import pytest
from src.smriti.upload.service import UploadService


@pytest.fixture(scope="function")
def service_deps():
    return (
        AsyncMock(name="store"),
        AsyncMock(name="txn_repo"),
        AsyncMock(name="media_repo"),
    )


async def test_should_create_upload_txn(service_deps):
    store, txn_repo, media_repo = service_deps

    service = UploadService(
        txn_repo=txn_repo, media_repo=media_repo, store=store
    )

    mock_txn = Mock(name="txn")
    txn_repo.create_new_txn.return_value = mock_txn
    txn = await service.create_txn(2)

    assert txn == mock_txn
    txn_repo.create_new_txn.assert_called_once_with(2)


async def test_should_upload_file(service_deps):
    store, txn_repo, media_repo = service_deps
    service = UploadService(
        txn_repo=txn_repo, media_repo=media_repo, store=store
    )

    mock_upload_file = Mock(name="file")
    mock_upload_file.file = "file_binary"
    mock_upload_file.filename = "filename"

    store.save_temporarily.return_value = "/saved/filepath"

    path = await service.upload_file("txn_id", "media1", mock_upload_file)

    store.save_temporarily.assert_called_once_with("file_binary", "filename")
    txn_repo.add_media.assert_called_once_with(
        "txn_id", "media1", "/saved/filepath"
    )
    assert path == "/saved/filepath"


async def test_should_commit_a_txn(service_deps):
    store, txn_repo, media_repo = service_deps
    service = UploadService(
        txn_repo=txn_repo, media_repo=media_repo, store=store
    )

    txn_mock = Mock(name="txn")
    txn_mock.file_paths = ["media/file/path"]
    txn_mock.mediaIds = ["media1"]

    txn_repo.get_txn.return_value = txn_mock
    store.save_permanently.return_value = ["/new/path"]

    await service.commit_txn("txn_id")

    txn_repo.get_txn.assert_called_once_with("txn_id")
    store.save_permanently.assert_called_once_with(["media/file/path"])
    media_repo.add_new_media.assert_called_once_with(["media1"], ["/new/path"])
