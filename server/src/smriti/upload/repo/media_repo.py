from ..models.media import Media


class MediaRepo:
    def __init__(self):
        self.db = {}

    async def add_new_media(self, media_ids: list[str], file_paths: list[str]):
        for media_id, file_path in zip(media_ids, file_paths):
            self.db[media_id] = Media(media_id=media_id, file_path=file_path)
