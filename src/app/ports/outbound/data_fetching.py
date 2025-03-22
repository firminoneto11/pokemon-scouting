from abc import ABCMeta, abstractmethod
from typing import TypedDict


class Data(TypedDict):
    name: str
    base_experience: int
    abilities: str
    weight: int
    raw_json: str


class DataFetcherPort(metaclass=ABCMeta):
    @abstractmethod
    async def get_info_for(self, name: str) -> Data | None: ...
