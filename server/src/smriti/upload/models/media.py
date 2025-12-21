from pydantic import BaseModel


class Media(BaseModel):
    media_id: str
    file_path: str
