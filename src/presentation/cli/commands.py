from functools import partial, wraps
from typing import Awaitable, Callable

import anyio
import uvicorn
from typer import Typer

from conf import settings

app = Typer()


def coroutine[**Spec, T](func: Callable[Spec, Awaitable[T]]):
    @wraps(func)
    def wrapper(*args: Spec.args, **kwargs: Spec.kwargs):
        return anyio.run(func=partial(func, *args, **kwargs))

    return wrapper


@app.command("sample")
@coroutine
async def sample():
    print("Hello World")


@app.command("runserver")
def runserver():
    uvicorn.run(
        settings.ASGI_APP,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.should_reload,
    )
