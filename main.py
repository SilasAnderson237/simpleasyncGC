from coinGeckoWrapper import CoinGeckoWrapper


def run():
    api = CoinGeckoWrapper()

    api.market_chart("bitcoin", "usd", "max")
    api.ohlc("bitcoin", "usd", "max")
    api.markets("usd")

    res = api.run()

    print(res)


if __name__ == "__main__":
    run()
