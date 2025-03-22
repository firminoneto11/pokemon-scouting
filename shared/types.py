from typing import TYPE_CHECKING, Literal, Protocol

from quart import Quart

if TYPE_CHECKING:
    from src.app.ports.outbound.database import SqlDBPort


type EnvChoices = Literal["development", "testing", "staging", "production", "ci"]


class StateProtocol(Protocol):
    db: "SqlDBPort"
    connected: bool


class ASGIApp(Quart):
    state: StateProtocol
