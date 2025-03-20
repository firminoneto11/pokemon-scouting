import json as jsonlib
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Literal, Optional, cast

from httpx import Client, Response

from shared.utils import retry_decorator

from .exceptions import InvalidHTTPStatusError

EXPECTED_CODES = (200,)


@dataclass
class HttpClient:
    base_url: str
    headers: Optional[dict[str, Any]] = None
    timeout: int = 15
    retries: int = 3
    retry_delay: int = 1
    exponential_delay: int = 2

    async def get(
        self,
        endpoint: str,
        query_params: Optional[dict[str, Any]] = None,
        expected_status_codes: tuple[int, ...] = EXPECTED_CODES,
        headers: Optional[dict[str, Any]] = None,
    ):
        return await self._make_request(
            method="GET",
            endpoint=endpoint,
            query_params=query_params,
            expected_status_codes=expected_status_codes,
            headers=headers,
        )

    async def post(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        query_params: Optional[dict[str, Any]] = None,
        expected_status_codes: tuple[int, ...] = EXPECTED_CODES,
        headers: Optional[dict[str, Any]] = None,
    ):
        raise

    async def _make_request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        query_params: Optional[dict[str, Any]] = None,
        expected_status_codes: tuple[int, ...] = EXPECTED_CODES,
        headers: Optional[dict[str, Any]] = None,
    ):
        if method.strip().upper() not in ("GET", "POST"):
            raise ValueError(f"The {method!r} method is not allowed")

        if json and data:
            raise ValueError("Can not set both 'json' and 'data'")

        headers_ = self.headers or dict()
        if headers:
            headers_ = {**headers, **headers_}

        fetch, err = (
            retry_decorator(
                times=self.retries,
                delay=self.retry_delay,
                exponential_delay=self.exponential_delay,
            )(self._fetch),
            None,
        )

        try:
            response = await fetch(
                client_kwargs={
                    "base_url": self.base_url,
                    "headers": headers_,
                    "timeout": self.timeout,
                },
                method=method,
                endpoint=endpoint,
                json=json,
                data=data,
                query_params=query_params,
                expected_status_codes=expected_status_codes,
            )
        except Exception as exc:
            response, err = Response(204), exc

        return response, err

    async def _fetch(
        self,
        client_kwargs: dict[str, Any],
        method: Literal["GET", "POST"],
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        query_params: Optional[dict[str, Any]] = None,
        expected_status_codes: tuple[int, ...] = (200,),
    ):
        kwargs = {}

        if json:
            kwargs["json"] = json
        if data:
            kwargs["data"] = data
        if query_params:
            kwargs["params"] = query_params

        with Client(**client_kwargs) as client:
            call = cast(
                Callable[..., Awaitable[Response]],
                getattr(client, method.strip().lower()),
            )
            response = await call(endpoint, **kwargs)

        if response.status_code in expected_status_codes:
            return response

        try:
            text = jsonlib.dumps(response.json())
        except:  # noqa
            text = response.text

        raise InvalidHTTPStatusError(
            detail=(
                f"The {endpoint!r} API returned an unexpected status code response: "
                f"{response.status_code!r}"
            ),
            response_text=text,
        )
