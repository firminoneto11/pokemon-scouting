import traceback
from datetime import datetime, timezone
from functools import lru_cache, wraps
from typing import Awaitable, Callable, Literal, overload

from anyio import sleep
from environs import Env
from uuid_extensions import uuid7  # type: ignore


@lru_cache(maxsize=1)
def get_env():
    (env := Env()).read_env()
    return env


def generate_uuid(as_hex: bool = False):  # type: ignore
    uuid = uuid7()
    if as_hex:
        return uuid.hex  # type: ignore
    return str(uuid)


@overload
def utc_timestamp(unix: Literal[False] = False) -> datetime: ...


@overload
def utc_timestamp(unix: Literal[True]) -> int: ...


def utc_timestamp(unix: bool = False):
    utc_now = datetime.now(tz=timezone.utc)
    if unix:
        utc_now = int(utc_now.timestamp())
    return utc_now


def retry_decorator(times: int, delay: int, exponential_delay: int = 2):
    def _inner[**Spec, T](function: Callable[Spec, Awaitable[T]]):
        @wraps(function)
        async def actual_decorator(*args: Spec.args, **kwargs: Spec.kwargs):
            if times <= 0:
                return await function(*args, **kwargs)

            backoff, err = delay, None

            try:
                return await function(*args, **kwargs)
            except Exception as exc:
                traceback.print_exc()
                err = exc

            if backoff:
                await sleep(backoff)
                backoff = backoff * exponential_delay

            for idx in range(times):
                try:
                    return await function(*args, **kwargs)
                except Exception as exc:
                    traceback.print_exc()
                    err = exc

                    if idx + 1 == times:
                        break

                    if backoff:
                        await sleep(backoff)
                        backoff = backoff * exponential_delay

            msg = Exception("Exhausted all of the retries")
            if err:
                raise msg from err
            raise msg

        return actual_decorator

    return _inner
