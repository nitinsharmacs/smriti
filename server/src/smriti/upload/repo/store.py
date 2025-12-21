from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

import aiofiles
import aiofiles.os

from ...constants import ROOT_DIR


class StorageBackend(ABC):
    @abstractmethod
    async def save(self, path: str, file: BinaryIO):
        pass

    @abstractmethod
    async def move(self, old_path: str, new_path: str):
        pass


class FileStore(StorageBackend):
    CHUNK_SIZE = 1024 * 1024 * 5  # 5MB

    async def save(self, path: str, file: BinaryIO):
        async with aiofiles.open(path, "+wb") as fob:
            while content := file.read(FileStore.CHUNK_SIZE):
                await fob.write(content)

    async def move(self, old_path: str, new_path: str):
        await aiofiles.os.replace(old_path, new_path)


class Store:
    def __init__(self, backend: StorageBackend) -> None:
        self.temp_location = "/tmp"
        self.permanent_location = f"{ROOT_DIR}/storage/images"
        self.backend = backend

    async def save_temporarily(
        self, file: BinaryIO, filename: str | None = "temp.file"
    ):
        filepath = f"{self.temp_location}/{filename}"
        await self.backend.save(filepath, file)
        return filepath

    async def save_permanently(self, file_paths: list[str]) -> list[str]:
        for old_path in file_paths:
            await self.backend.move(
                old_path, self.permanent_location + "/" + Path(old_path).name
            )
        return []
