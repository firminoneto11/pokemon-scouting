from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, cast

from loguru import logger
from quart import Quart

from conf import settings
from src.infra.database import SqlDBAdapter

from .handlers import get_exception_handlers
from .routers import get_routers

if TYPE_CHECKING:
    from shared.types import ASGIApp, StateProtocol
    from src.app.ports.outbound.database import SqlDBPort


@dataclass
class State:
    db: "SqlDBPort"
    connected: bool


class ASGIFactory:
    _apps_stack: list["ASGIApp"] = []

    @classmethod
    def new(cls):
        application = cls().application
        cls._apps_stack.append(application)
        return application

    @classmethod
    def latest_app(cls):
        return cls._apps_stack[-1]

    def __init__(self):
        self.application = cast("ASGIApp", Quart(__name__))

        self.configure_logging()
        self.configure_state()
        self.configure_lifespan()
        self.configure_middleware()
        self.configure_exception_handlers()
        self.configure_routers()

    def configure_logging(self): ...

    def configure_state(self):
        self.application.state = State(
            db=SqlDBAdapter(connection_string=settings.DATABASE_URL),
            connected=False,
        )

    def configure_lifespan(self):
        self.application.before_serving(
            partial(self._on_startup, self.application.state)
        )
        self.application.after_serving(
            partial(self._on_shutdown, self.application.state)
        )

    def configure_middleware(self): ...

    def configure_exception_handlers(self):
        for error, handler in get_exception_handlers().items():
            self.application.errorhandler(error)(handler)

    def configure_routers(self):
        for router in get_routers():
            self.application.register_blueprint(router)

    async def _on_startup(self, state: "StateProtocol"):
        if not state.connected:
            await state.db.connect()
            state.connected = True
            logger.info("Connected to the database")

    async def _on_shutdown(self, state: "StateProtocol"):
        if state.connected:
            await state.db.disconnect()
            state.connected = False
            logger.info("Disconnected from the database")


app = ASGIFactory.new()
