from quart import Blueprint as Router

from conf import settings

from .controllers.v1 import V1_ROUTERS


def get_routers():
    v1 = Router("v1", __name__, url_prefix=f"/{settings.API_PREFIX}/v1")

    for value in V1_ROUTERS.values():
        v1.register_blueprint(value)

    return [v1]
