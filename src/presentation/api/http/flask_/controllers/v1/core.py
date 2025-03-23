from typing import TYPE_CHECKING

from quart import Blueprint as Router
from quart import request

from src.app.services.core import CoreService
from src.infra.data_fetching import DataFetcherAdapter
from src.infra.repositories.pokemons import PokemonRepo

from ..utils import inject_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = Router("pokemons", __name__)


@router.get("/pokemons")
@inject_session
async def get_pokemon_details(session: "AsyncSession"):
    if not (pokemon := request.args.get("name", default=None, type=str)):
        return {
            "detail": "You must specify a pokemon name using the 'name' query string"
        }, 400

    svc = CoreService(
        pokemon_repo=PokemonRepo(session=session),
        data_fetcher=DataFetcherAdapter(backend="pokeapi"),
    )

    return await svc.get_pokemon_details(name=pokemon), 200
