from typing import TYPE_CHECKING

from pytest import mark

from src.app.services.core import CoreService
from src.infra.repositories.pokemons import PokemonRepo

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from tests.src.app.conftest import DataFetcherAdapterMock


class TestCoreService:
    def setup_class(self):
        print("Setting up")

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

        result = await svc.get_pokemon_details(name=pokemon)

        assert result["name"] == pokemon

    def teardown_class(self):
        print("Tearing down")
