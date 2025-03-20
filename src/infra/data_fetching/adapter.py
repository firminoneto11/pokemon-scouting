from typing import Literal, cast

from src.app.ports.outbound.data_fetching import DataFetcherPort

from .base_backend import BaseAPIBackend
from .pokeapi_backend import PokeAPIBackend

type Backends = Literal["pokeapi"]


class DataFetcherAdapter(DataFetcherPort):
    _ALLOWED_BACKENDS = {"pokeapi"}

    def __init__(self, backend: Backends):
        if backend not in self._ALLOWED_BACKENDS:
            raise ValueError(
                (
                    f"Invalid value for the data api backend. Allowed values are "
                    f"{self._ALLOWED_BACKENDS}"
                )
            )
        self._backend = backend
        self._client = self._get_client()

    @property
    def backend(self):
        return cast(Backends, self._backend)

    @property
    def client(self):
        return self._client

    async def get_info_for(self, name: str):
        return await self.client.get_info_for(name=name)

    def _get_client(self):
        clients = {"pokeapi": PokeAPIBackend}
        return cast(BaseAPIBackend, clients[self.backend]())
