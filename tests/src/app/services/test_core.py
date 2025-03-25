from typing import TYPE_CHECKING

from pytest import mark
from sqlalchemy import func, select

from src.app.services.core import CoreService
from src.domain.models import Pokemon
from src.infra.repositories.pokemons import PokemonRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from tests.src.app.conftest import DataFetcherAdapterMock


class TestCoreService:
    async def count_pokemons(self, session: "AsyncSession"):
        stmt = select(func.count()).select_from(Pokemon)
        return (await session.scalars(stmt)).one()

    @mark.parametrize(argnames="pokemon", argvalues=["pikachu", "charizard"])
    async def test_get_pokemon_details(
        self,
        session: "AsyncSession",
        data_fetcher_mock: "DataFetcherAdapterMock",
        pokemon: str,
    ):
        svc = CoreService(
            pokemon_repo=PokemonRepo(session=session), data_fetcher=data_fetcher_mock
        )

        amount_before = await self.count_pokemons(session=session)
        result = await svc.get_pokemon_details(name=pokemon)
        amount_after = await self.count_pokemons(session=session)

        assert not amount_before
        assert amount_after == 1
        assert isinstance(result["id"], str)
        assert result["name"] == pokemon
        assert isinstance(result["base_experience"], int)
        assert isinstance(result["abilities"], list)
        assert isinstance(result["weight"], int)
