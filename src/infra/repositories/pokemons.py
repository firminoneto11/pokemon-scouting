from typing import TYPE_CHECKING

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.ports.outbound.repos import PokemonRepoPort
from src.domain.models import Pokemon

if TYPE_CHECKING:
    from src.app.ports.outbound.data_fetching import Data


class PokemonRepo(PokemonRepoPort):
    session: AsyncSession

    async def get_by_name(self, name: str):
        stmt = select(Pokemon).where(func.lower(Pokemon.name) == name.lower().strip())
        return (await self.session.scalars(stmt)).first()

    async def create(self, data: "Data"):
        instance = Pokemon(**data)
        await self.session.flush(objects=[instance])
        return instance
