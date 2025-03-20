from contextlib import asynccontextmanager
from functools import lru_cache
from typing import TYPE_CHECKING

from conf import settings
from src.app.ports.outbound.database import SqlDBPort

from .sqlalchemy_backend import Database as SqlAlchemyDatabase

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


@lru_cache(typed=True)
def _get_database(connection_string: str):
    return SqlAlchemyDatabase(connection_string, always_commit=settings.autocommit)


class SqlDBAdapter(SqlDBPort):
    def __init__(self, connection_string: str):
        self._database = _get_database(connection_string)

    @property
    def engine(self):
        return self.database.engine

    @property
    def database(self):
        return self._database

    async def connect(
        self, echo_sql: bool = False, pool_size: int = 5, max_overflow: int = 5
    ):
        await self.database.connect(
            echo_sql=echo_sql, pool_size=pool_size, max_overflow=max_overflow
        )

    async def disconnect(self):
        await self.database.disconnect()

    @asynccontextmanager
    async def begin_session(self):
        async with self.database.begin_session() as session:
            yield session

    async def ping(self):
        await self.database.ping()

    async def migrate(self, base_model: "type[DeclarativeBase]", drop: bool = False):
        await self.database.migrate(base_model=base_model, drop=drop)
