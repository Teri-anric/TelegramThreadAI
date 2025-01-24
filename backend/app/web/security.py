from typing import Coroutine
from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security import APIKeyHeader


class APIKeyAuth(APIKeyHeader):
    """
    API key authentication.
    """

    def __init__(
        self,
        name: str,
        scheme_name: str,
        auto_error: bool = True,
        name_in_cookie: str | None = None,
        name_in_query: str | None = None,
    ):
        super().__init__(name=name, scheme_name=scheme_name, auto_error=auto_error)
        self.name_in_cookie = name_in_cookie
        self.name_in_query = name_in_query

    def get_api_key(self, request: Request):
        api_key = request.headers.get(self.model.name)
        if not api_key and self.name_in_cookie:
            api_key = request.cookies.get(self.name_in_cookie)
        if not api_key and self.name_in_query:
            api_key = request.query_params.get(self.name_in_query)
        return api_key

    def __call__(self, request: Request):
        api_key = self.get_api_key(request)
        if not api_key:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return api_key


oauth2_scheme = APIKeyAuth(
    name="x-token",
    scheme_name="Bearer",
    name_in_cookie="access_token",
    name_in_query="x-token",
)
