from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models import Pokemon

    from ..data_fetching import Data


class PokemonRepoPort:
    async def get_by_name(self, name: str) -> "Pokemon | None": ...

    async def create(self, data: "Data") -> "Pokemon": ...
