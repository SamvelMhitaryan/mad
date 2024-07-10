from pydantic import BaseModel


class FileSchema(BaseModel):
    id: int
    file_url: str
    file_name: str
    content_type: str
    size: int

    class Config:
        from_attributes = True
