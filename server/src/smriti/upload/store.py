from abc import ABC, abstractmethod
from typing import BinaryIO

import aiofiles


class StorageBackend(ABC):
    @abstractmethod
    async def save(self, path: str, file: BinaryIO):
        pass


class FileStore(StorageBackend):
    CHUNK_SIZE = 1024 * 1024 * 5  # 5MB

    async def save(self, path: str, file: BinaryIO):
        async with aiofiles.open(path, "+wb") as fob:
            while content := file.read(FileStore.CHUNK_SIZE):
                await fob.write(content)


class Store:
    def __init__(self, backend: StorageBackend) -> None:
        self.backend = backend

    async def save_temporarily(
        self, file: BinaryIO, filename: str | None = "temp.file"
    ):
        filepath = f"/tmp/{filename}"
        await self.backend.save(filepath, file)
        return filepath
