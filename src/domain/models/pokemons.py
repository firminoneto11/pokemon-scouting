import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimeStampedBaseModel


class Pokemon(TimeStampedBaseModel):
    __tablename__ = "pokemons"

    name: Mapped[str] = mapped_column(sa.String(50), index=True, unique=True)
    base_experience: Mapped[int] = mapped_column(sa.Integer)
    abilities: Mapped[str] = mapped_column(sa.String)
    weight: Mapped[int] = mapped_column(sa.Integer)
    raw_json: Mapped[str] = mapped_column(sa.String)

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_experience": self.base_experience,
            "abilities": self.abilities.split(","),
            "weight": self.weight,
        }
