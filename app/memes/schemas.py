from pydantic import BaseModel


class MemeBase(BaseModel):
    title: str
    image_url: str


class MemeCreate(MemeBase):
    pass


class Meme(MemeBase):
    id: int

    class Config:
        from_attributes = True
