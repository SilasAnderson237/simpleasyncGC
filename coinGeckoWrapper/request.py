import httpx

import asyncio
from enum import Enum, auto


Parameters = dict[str, str | int | float | bool | None]


class Status(Enum):
    UNSENT = auto()
    PENDING = auto()
    FAILED = auto()
    SUCCEEDED = auto()


class Request:
    """A request to the CoinGecko API."""

    def __init__(
        self,
        base_url: str,
        endpoint: str,
        params: Parameters | None = {},
        format_callback=None,
    ):
        """Initialize the request."""

        self._params = params
        self._status: Status = Status.UNSENT
        self._url: str = base_url + endpoint
        self.format_callback = format_callback

    @property
    def status(self) -> Status:
        """Get the status of the request."""

        return self._status

    async def _send_async(self):
        """Asyncronously send the request to the api."""

        self._status = Status.PENDING

        # send the request
        async with httpx.AsyncClient() as session:
            response = await session.get(self._url, params=self._params, timeout=200)

        # check whether the request failed
        if response.status_code != 200:
            self._status = Status.FAILED

            return response.json()

        self._status = Status.SUCCEEDED

        # check if the user provided a format callback
        if self.format_callback:
            return self.format_callback(response.json())

        return response.json()

    async def get_task(self):
        """Make task out of the request."""

        return await asyncio.create_task(self._send_async())

    def __repr__(self) -> str:
        """Get the representation of the request."""

        return f"<Request url={self._url} params={self._params} status={self._status}>"
