import json as jsonlib
from typing import Any


class BaseExc(Exception):
    def __init__(self, detail: str | dict[str, Any], code: int = 400):
        self.code = code

        if isinstance(detail, dict):
            self.detail = jsonlib.dumps(detail)
        else:
            self.detail = detail

        super().__init__(self.detail)


class ServiceException(BaseExc): ...
