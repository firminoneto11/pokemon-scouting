from typing import TYPE_CHECKING, Iterable, TypedDict, cast

from quart_cors import cors  # type: ignore

if TYPE_CHECKING:
    from quart import Blueprint, Quart


class CorsConfig(TypedDict):
    allow_credentials: bool
    allow_headers: Iterable[str]
    allow_methods: Iterable[str]
    allow_origin: Iterable[str]


cors_middleware_configuration = cast(
    CorsConfig,
    {
        "allow_credentials": False,
        "allow_headers": ["*"],
        "allow_methods": ["*"],
        "allow_origin": "*",
    },
)


def setup_cors[T: "Quart | Blueprint"](app_or_blueprint: T):  # type: ignore
    return cors(app_or_blueprint, **cors_middleware_configuration)
