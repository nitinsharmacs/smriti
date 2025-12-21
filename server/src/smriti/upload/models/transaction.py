from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    mediaIds: list[str] = []
    file_paths: list[str] = []

    def add_media(self, media_id: str, file_path: str):
        self.mediaIds.append(media_id)
        self.file_paths.append(file_path)
