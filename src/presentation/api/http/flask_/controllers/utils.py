from functools import lru_cache, wraps
from typing import TYPE_CHECKING, Awaitable, Callable, cast

from quart import current_app

if TYPE_CHECKING:
    from shared.types import ASGIApp


@lru_cache(maxsize=1)
def get_db_adapter():
    app = cast("ASGIApp", current_app)
    return app.state.db


def inject_session[**Spec, T](function: Callable[Spec, Awaitable[T]]):
    @wraps(function)
    async def actual_decorator(*args: Spec.args, **kwargs: Spec.kwargs):
        database = get_db_adapter()
        async with database.begin_session() as session:
            kwargs["session"] = session
            return await function(*args, **kwargs)

    return actual_decorator
