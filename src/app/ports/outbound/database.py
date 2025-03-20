from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, AsyncContextManager

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from sqlalchemy.orm import DeclarativeBase


class SqlDBPort(metaclass=ABCMeta):
    @property
    @abstractmethod
    def engine(self) -> "AsyncEngine": ...

    @abstractmethod
    async def connect(
        self, echo_sql: bool = False, pool_size: int = 5, max_overflow: int = 5
    ) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    def begin_session(self) -> AsyncContextManager["AsyncSession"]: ...

    @abstractmethod
    async def ping(self) -> None: ...

    @abstractmethod
    async def migrate(
        self, base_model: "type[DeclarativeBase]", drop: bool = False
    ) -> None: ...
