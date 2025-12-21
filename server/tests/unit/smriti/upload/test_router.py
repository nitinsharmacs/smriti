from unittest.mock import ANY, AsyncMock, Mock, patch
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
import pytest

from src.smriti.upload.router import create_router


@pytest.fixture(scope="function")
@patch("src.smriti.upload.router.MediaRepo")
@patch("src.smriti.upload.router.FileStore")
@patch("src.smriti.upload.router.Store")
@patch("src.smriti.upload.router.TxnRepo")
@patch("src.smriti.upload.router.UploadService")
def resources(mock_upload_service, _, __, ___, ____):
    upload_service_mock = AsyncMock(name="upload_service")
    mock_upload_service.return_value = upload_service_mock

    test_app = FastAPI()
    test_app.include_router(create_router())
    test_client = TestClient(test_app)

    return test_client, upload_service_mock


def test_should_create_upload_txn(resources):
    test_client, upload_service_mock = resources

    txn = Mock(name="txn")
    txn.id = "txn_id"
    txn.mediaIds = ["media1"]

    upload_service_mock.create_txn.return_value = txn

    result = test_client.post("/upload/create-txn", json={"mediaCount": 1})

    res_json = result.json()

    assert res_json["status"] == 201
    assert res_json["txnId"] == "txn_id"
    assert res_json["mediaIds"] == ["media1"]

    upload_service_mock.create_txn.assert_called_once_with(1)


def test_should_upload_file(resources):
    test_client, upload_service_mock = resources

    upload_service_mock.upload_file.return_value = "/uploaded/file/path"

    files = {"file": ("test_file.txt", b"test_file_content", "text/plain")}

    result = test_client.post(
        "/upload/upload",
        data={"txnId": "txn_id", "mediaId": "media_id"},
        files=files,
    )

    assert result.status_code == 200

    res_json = result.json()

    assert res_json["status"] == 201
    assert res_json["filepath"] == "/uploaded/file/path"

    actual_txn_id, actual_media_id, actual_file = (
        upload_service_mock.upload_file.call_args[0]
    )

    assert actual_txn_id == "txn_id"
    assert actual_media_id == "media_id"
    assert actual_file.filename == "test_file.txt"


def test_should_commit_upload(resources):
    test_client, upload_service_mock = resources

    result = test_client.put("/upload/commit", json={"txn_id": "txn_id"})

    assert result.status_code == 200

    res_json = result.json()

    assert res_json["status"] == 201
    assert res_json["txn_id"] == "txn_id"

    upload_service_mock.commit_txn.assert_called_once_with("txn_id")
