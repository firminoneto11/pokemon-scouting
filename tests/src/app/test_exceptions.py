import json as jsonlib
from typing import Any

from pytest import mark

from src.app.exceptions import BaseExc


@mark.parametrize(
    argnames=["detail_input", "code_input", "expected_detail"],
    argvalues=[
        ("testing1", 200, "testing1"),
        ("testing2", 300, "testing2"),
        ("testing3", 300, "testing3"),
        ({"detail": "testing4"}, 400, jsonlib.dumps({"detail": "testing4"})),
    ],
)
def test_base_exception(
    detail_input: str | dict[str, Any], code_input: int, expected_detail: str
):
    exc = BaseExc(detail=detail_input, code=code_input)
    assert exc.detail == expected_detail
    assert exc.code == code_input
