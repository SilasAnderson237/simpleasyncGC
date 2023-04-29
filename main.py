import pandas as pd
import matplotlib.pyplot as plt

from coinGeckoWrapper import CoinGeckoWrapper
from coinGeckoWrapper import CoinGeckoFormatter


def run():
    api = CoinGeckoWrapper()
    formatter = CoinGeckoFormatter()

    # api.market_chart("bitcoin", "usd", "max")
    # api.ohlc("bitcoin", "usd", "max")
    api.ping()

    res = api.get_requests()

    df = res

    print(df)

    # # define a lambda function to normalize each column
    # normalize = lambda col: (col - col.min()) / (col.max() - col.min())

    # # apply the normalization function to each column
    # df_norm = df.apply(normalize)

    # df_norm.plot()

    # plt.show()


if __name__ == "__main__":
    run()
