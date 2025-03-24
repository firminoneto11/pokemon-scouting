from unittest.mock import patch

from loguru import logger
from pytest import fixture
from uvloop import EventLoopPolicy

from conf import settings
from src.domain.models import TimeStampedBaseModel
from src.infra.database import SqlDBAdapter


@fixture(scope="session", autouse=True)
def event_loop_policy():
    return EventLoopPolicy()


@fixture(scope="session", autouse=True)
async def database():
    db = SqlDBAdapter(connection_string=settings.DATABASE_URL)
    await db.connect()
    logger.info("Connected to the database")
    try:
        yield db
    finally:
        await db.disconnect()
        logger.info("Disconnected from the database")


@fixture(scope="session", autouse=True)
async def migrate(database: SqlDBAdapter):
    await database.migrate(base_model=TimeStampedBaseModel)
    logger.info("Migrated all the models for testing")


@fixture
async def session(database: SqlDBAdapter):
    async with database.begin_session() as session:
        with patch.object(target=session, attribute="commit", new=session.flush):
            try:
                yield session
            finally:
                await session.rollback()
