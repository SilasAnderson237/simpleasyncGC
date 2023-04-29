import asyncio
from typing import Callable

from .request import Request, Status
from .formatter import CoinGeckoFormatter as fm


Parameters = dict[str, str | int | float | bool | None]

ENDPOINTS: dict[str, str] = {
    # ping
    "ping": "ping",
    # simple
    "price": "simple/price",
    "supported_vs_currencies": "simple/supported_vs_currencies",
    # coin endpoints
    "list_coins": "coins/list",
    "markets": "coins/markets",
    "ohlc": "coins/{id}/ohlc",
    "market_chart": "coins/{id}/market_chart",
}


class CoinGeckoWrapper:
    """CoinGecko API wrapper."""

    BASE_URL = "https://api.coingecko.com/api/v3/"

    def __init__(self, vs_currency: str = "usd") -> None:
        self.vs_currency: str = vs_currency
        self.requests: list[Request] = []

    # ----------------------UTILS-----------------------

    def _make_parameters(self, args) -> Parameters:
        """Turns the args into a dict with the correct format."""

        parameters: Parameters = {}

        for key, val in args:
            if key == "kwargs":
                parameters.update(val)

            elif key != "self" and key != "format_callback" and val is not None:
                parameters.update({key: val})

        return parameters

    async def _gather(self):
        """Gathers all the tasks"""

        return await asyncio.gather(*[req.get_task() for req in self.requests])

    def get_requests(self):
        """Runs all the tasks"""

        result = asyncio.run(self._gather())

        self.requests = [req for req in self.requests if req.status != Status.SUCCEEDED]

        return result

    # ---------------------REQUESTS---------------------

    def _add_request(
        self, endpoint: str, data: dict | None = None, format_callback=None
    ) -> None:
        """Add a request to the list of unsent requests."""

        self.requests.append(Request(self.BASE_URL, endpoint, data, format_callback))

    # -----------------------PING-----------------------

    def ping(self) -> None:
        """Check API server status."""

        self._add_request(endpoint=ENDPOINTS["ping"])

    # -----------------SIMPLE ENDPOINTS-----------------

    def price(
        self, ids: str, vs_currencies: str, format_callback=fm.price_formatter, **kwargs
    ) -> None:
        """Get the current price of any cryptocurrencies in any other supported currencies that you need."""

        self._add_request(
            endpoint=ENDPOINTS["price"],
            data=self._make_parameters(locals().items()),
            format_callback=format_callback,
        )

    def supported_vs_currencies(self) -> None:
        """Get list of supported_vs_currencies."""

        self._add_request(endpoint=ENDPOINTS["supported_vs_currencies"])

    # -----------------COINS ENDPOINTS------------------

    def list_coins(
        self,
        include_platform: bool = False,
        format_callback: Callable = fm.list_coins_formatter,
        **kwargs,
    ) -> None:
        """Use this to obtain all the coins' id in order to make API calls."""

        self._add_request(
            endpoint=ENDPOINTS["list_coins"],
            data=self._make_parameters(locals().items()),
            format_callback=format_callback,
        )

    def markets(
        self,
        vs_currency: str,
        format_callback: Callable = fm.markets_formatter,
        **kwargs,
    ) -> None:
        """Use this to obtain all the coins market data (price, market cap, volume)."""

        self._add_request(
            endpoint=ENDPOINTS["markets"],
            data=self._make_parameters(locals().items()),
            format_callback=format_callback,
        )

    def market_chart(
        self,
        id: str,
        vs_currency: str,
        days: str,
        format_callback: Callable = fm.market_chart_formatter,
        **kwargs,
    ) -> None:
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""

        self._add_request(
            endpoint=ENDPOINTS["market_chart"].format(id=id),
            data=self._make_parameters(locals().items()),
            format_callback=format_callback,
        )

    def ohlc(
        self,
        id: str,
        vs_currency: str,
        days: str,
        format_callback: Callable = fm.ohlc_formatter,
        **kwargs,
    ) -> None:
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""

        self._add_request(
            endpoint=ENDPOINTS["ohlc"].format(id=id),
            data=self._make_parameters(locals().items()),
            format_callback=format_callback,
        )

    # ----------------CONTRACT ENDPOINTS----------------
    # ------------ASSET_PLATFORMS ENDPOINTS-------------
    # ---------------CATEGORIES ENDPOINTS---------------
    # ---------------EXCHANGES ENDPOINTS----------------
    # ----------------INDEXES ENDPOINTS-----------------
    # --------------DERIVATIVES ENDPOINTS---------------
    # ------------------NFTS ENDPOINTS------------------
    # -------------EXCHANGE_RATES ENDPOINTS-------------
    # -----------------SEARCH ENDPOINTS-----------------
    # ----------------TRENDING ENDPOINTS----------------
    # -----------------GLOBAL ENDPOINTS-----------------
    # ---------------COMPANIES ENDPOINTS----------------
