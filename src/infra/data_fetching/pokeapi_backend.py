import json as jsonlib
from typing import TYPE_CHECKING, Any, cast

from src.infra.http_client import HttpClient

from .base_backend import BaseAPIBackend

if TYPE_CHECKING:
    from src.app.ports.outbound.data_fetching import Data


class PokeAPIBackend(BaseAPIBackend):
    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(self):
        self.client = HttpClient(base_url=self.BASE_URL)

    async def get_info_for(self, name: str):
        response, err = await self.client.get(endpoint=f"/pokemon/{name}")

        if err:
            return

        return self._transform(data=response.json())

    def _transform(self, data: dict[str, Any]):
        transformed = {
            "name": data["name"],
            "base_experience": data["base_experience"],
            "abilities": ",".join([el["ability"]["name"] for el in data["abilities"]]),
            "weight": data["weight"],
            "raw_json": jsonlib.dumps(data),
        }

        return cast("Data", transformed)
