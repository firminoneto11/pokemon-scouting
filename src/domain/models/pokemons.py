import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimeStampedBaseModel


class Pokemon(TimeStampedBaseModel):
    __tablename__ = "pokemons"

    name: Mapped[str] = mapped_column(sa.String(50), index=True, unique=True)

    def dump(self):
        return {
            "name": self.name,
        }
