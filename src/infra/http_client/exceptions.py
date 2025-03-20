import json as jsonlib
from typing import Optional


class BaseException(Exception):
    def __init__(self, detail: str, response_text: Optional[str] = None):
        self.detail = detail
        self.response_text = response_text
        super().__init__(self.error_message)

    @property
    def error_message(self):
        error = {"detail": self.detail}
        if self.detail and self.response_text:
            error["response"] = self.response_text
        return jsonlib.dumps(error, indent=2)


class InvalidHTTPStatusError(BaseException): ...
