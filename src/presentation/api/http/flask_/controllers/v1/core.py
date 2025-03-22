from typing import TYPE_CHECKING

from quart import Blueprint as Router
from quart import request

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router("stocks", __name__)


@router.get("/pokemons")
async def get_pokemon_details(session: AsyncSession):
    if not (pokemon := request.args.get("name", default=None, type=str)):
        return {
            "detail": "You must specify a pokemon name using the 'name' query string"
        }, 400

    return {"detail": f"Your pokemon is {pokemon}"}, 200
