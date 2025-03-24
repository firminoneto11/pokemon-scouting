import json as jsonlib
from functools import lru_cache
from typing import cast

from faker import Faker
from pytest import fixture

from src.app.ports.outbound.data_fetching import Data, DataFetcherPort


@lru_cache(typed=True, maxsize=None)
def _create_random_pokemon(name: str):
    return {
        "name": name,
        "base_experience": faker.random_int(),
        "abilities": ",".join(
            [faker.word() for _ in range(faker.random_int(min=1, max=10))]
        ),
        "weight": faker.random_int(),
    }


class DataFetcherAdapterMock(DataFetcherPort):
    async def get_info_for(self, name: str):
        data = _create_random_pokemon(name=name)
        data["raw_json"] = jsonlib.dumps(data)
        return cast(Data, data)


@fixture
def data_fetcher_mock():
    return DataFetcherAdapterMock()


faker = Faker()
