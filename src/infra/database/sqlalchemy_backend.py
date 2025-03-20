import gc
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from sqlalchemy.orm import DeclarativeBase


class Database:
    _connection_string: str
    _always_commit: bool

    _engine: Optional["AsyncEngine"]
    _start_db_session: Optional[async_sessionmaker["AsyncSession"]]
    _active_sessions: set["AsyncSession"]
    _is_connected: bool

    def __init__(self, connection_string: str, always_commit: bool = True):
        self._connection_string = connection_string
        self._always_commit = always_commit
        self._set_defaults()

    @property
    def engine(self):
        if self._engine is None:
            raise ValueError("'_engine' is None. Can not proceed")
        return self._engine

    @property
    def start_db_session(self):
        if self._start_db_session is None:
            raise ValueError("'_start_db_session' is None. Can not proceed")
        return self._start_db_session

    @property
    def active_sessions(self):
        return self._active_sessions

    @property
    def using_sqlite(self):
        return self._connection_string.startswith("sqlite")

    async def connect(
        self, echo_sql: bool = False, pool_size: int = 5, max_overflow: int = 5
    ):
        if self._is_connected:
            return

        kws: dict[str, Any] = dict()
        if self.using_sqlite:
            kws["connect_args"] = {"check_same_thread": False}
        else:
            kws["pool_size"] = pool_size
            kws["max_overflow"] = max_overflow

        self._engine = create_async_engine(
            url=self._connection_string, echo=echo_sql, **kws
        )

        self._start_db_session = async_sessionmaker(
            self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

        await self._check_connection()

    async def disconnect(self):
        if not self._is_connected:
            return

        try:
            [await session.close() for session in self.active_sessions]
            await self.engine.dispose()
        finally:
            self._set_defaults(cleanup=True)

    @asynccontextmanager
    async def begin_session(self):
        self._validate_connection()
        async with self.start_db_session() as session:
            self.active_sessions.add(session)
            try:
                yield session
            except Exception as exc:
                await session.rollback()
                raise exc
            else:
                if self._always_commit:
                    await session.commit()
            finally:
                self.active_sessions.remove(session)

    async def ping(self):
        try:
            async with self.begin_session() as session:
                await session.execute(text("SELECT 1;"))
        except Exception as exc:
            raise ConnectionError("Failed to ping the database") from exc

    async def migrate(self, base_model: "type[DeclarativeBase]", drop: bool = False):
        self._validate_connection()

        async with self.engine.begin() as conn:
            if drop:
                await conn.run_sync(base_model.metadata.drop_all)
            await conn.run_sync(base_model.metadata.create_all)

            # NOTE: This option has to be enabled in order to use foreign key
            # constraints for sqlite. Check:
            # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
            if self.using_sqlite:
                await conn.execute(text("PRAGMA foreign_keys=ON"))

    def _validate_connection(self):
        if not self._is_connected:
            raise ConnectionError("This instance is not connected to the database yet")

    async def _check_connection(self):
        self._is_connected = True
        try:
            await self.ping()
        except ConnectionError as exc:
            await self.disconnect()
            raise ConnectionError("Failed to connect to the database") from exc

    def _set_defaults(self, cleanup: bool = False):
        self._engine = None
        self._start_db_session = None
        self._active_sessions = set()
        self._is_connected = False

        if cleanup:
            gc.collect()
