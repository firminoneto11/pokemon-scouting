from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.ports.outbound.data_fetching import Data


class BaseAPIBackend(metaclass=ABCMeta):
    @abstractmethod
    async def get_info_for(self, name: str) -> "Data | None": ...
