import json

from requests import Response as RequestResponse


class Response:
    def __init__(self, data, is_error=False):
        self.data = data
        self.is_error = is_error

    def err(self):
        return self.is_error

    def ok(self):
        return not self.err()

    def __str__(self) -> str:
        return json.dumps(self.data, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    @classmethod
    def process(cls, response: RequestResponse) -> "Ok | Err":
        if response.ok:
            return Ok(
                {
                    "status_code": response.status_code,
                    "reason": response.reason,
                    "json": response.json(),
                }
            )
        else:
            err = {
                "status_code": response.status_code,
                "reason": response.reason,
                "text": response.text,
            }
            try:
                Err(err | {"json": response.json()})
            except:
                return Err(err)


class Ok(Response):
    def __init__(self, response):
        super().__init__(response, False)


class Err(Response):
    def __init__(self, response):
        super().__init__(response, True)
