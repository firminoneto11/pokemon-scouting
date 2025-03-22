from dataclasses import dataclass

from ..exceptions import ServiceException
from ..ports.outbound.data_fetching import DataFetcherPort
from ..ports.outbound.repos import PokemonRepoPort


@dataclass
class CoreService:
    pokemon_repo: PokemonRepoPort
    data_fetcher: DataFetcherPort

    async def get_pokemon_details(self, name: str):
        name_ = name.strip().lower()
        if (pokemon := await self.pokemon_repo.get_by_name(name=name_)) is None:
            if (data := await self.data_fetcher.get_info_for(name=name_)) is None:
                raise ServiceException(detail="Pokemon not found", code=404)

            pokemon = await self.pokemon_repo.create(data=data)

        return pokemon.dump()
