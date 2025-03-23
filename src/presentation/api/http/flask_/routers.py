from typing import Callable, TypeVar

from quart import Blueprint as Router

from conf import settings

from .controllers.v1 import V1_ROUTERS

RouterInput = TypeVar("RouterInput", bound=Router)
FuncType = Callable[[RouterInput], RouterInput]


def get_routers(setup_cors: FuncType[Router]):
    v1 = setup_cors(Router("v1", __name__, url_prefix=f"/{settings.API_PREFIX}/v1"))

    for value in V1_ROUTERS.values():
        v1.register_blueprint(setup_cors(value))

    return [v1]
