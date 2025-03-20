import tomllib
from pathlib import Path
from typing import cast

from shared.types import EnvChoices
from shared.utils import get_env

with open("pyproject.toml", mode="rb") as stream:
    pyproject = tomllib.load(stream)


ENV_PREFIX = "POKEMON_SCOUTING_"


with get_env().prefixed(ENV_PREFIX) as env:

    class Conf:
        BASE_DIR = Path(__file__).parent.parent

        ENVIRONMENT_PREFIX = ENV_PREFIX

        ENVIRONMENT = cast(EnvChoices, env.str("ENVIRONMENT", "development"))

        APP_NAME = pyproject["project"]["name"]
        APP_DESCRIPTION = pyproject["project"]["description"]
        APP_VERSION = pyproject["project"]["version"]

        DEBUG = env.bool("DEBUG", False)

        API_PREFIX = "/api"

        ASGI_APP = "src.presentation.api.http.flask_.asgi:app"
        HOST = env.str("HOST", "127.0.0.1")
        PORT = env.int("PORT", 8000)

        DATABASE_URL = env.str("DATABASE_URL", "changeMe")

        @property
        def autocommit(self):
            return self.ENVIRONMENT != "testing"

        @property
        def should_reload(self):
            return self.ENVIRONMENT == "development"
