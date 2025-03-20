class BaseException(Exception):
    def __init__(self, detail: str, code: int = 400):
        self.code = code
        self.detail = detail
        super().__init__(detail)


class GenericException(BaseException): ...
