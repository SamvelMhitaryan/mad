from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.memes.database import Base


class Meme(Base):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(70))
    file_id: Mapped[int] = mapped_column(nullable=False)
