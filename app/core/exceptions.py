"""
API 커스텀 Exception
"""

from app.core.responses import APIResponseCode


class APIException(Exception):
    def __init__(self, response_code: APIResponseCode, context: dict = None):
        self.response_code = response_code
        self.status_code = response_code.status
        self.context = context or {}
        super().__init__(
            f"API Error: {response_code.code} - {response_code.description}"
        )

    @property
    def code(self) -> APIResponseCode:
        return self.response_code

    @property
    def http_status(self) -> int:
        return self.status_code
