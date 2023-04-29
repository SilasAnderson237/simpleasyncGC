import pandas as pd


class CoinGeckoFormatter:
    """Formats data from the CoinGecko API into pandas dataframes."""

    @staticmethod
    def price_formatter(data: dict) -> pd.DataFrame:
        """Formats the data from the price endpoint into a pandas dataframe."""

        # create dataframe without mentioning columns
        df = pd.DataFrame(data)

        return df

    @staticmethod
    def list_coins_formatter(data: dict) -> pd.DataFrame:
        """Formats the data from the list_coins endpoint into a pandas dataframe."""

        # create dataframe without mentioning columns
        df = pd.DataFrame(data)

        # set the index to the id column
        df.set_index("id", inplace=True, drop=False)

        return df

    @staticmethod
    def markets_formatter(data: dict) -> pd.DataFrame:
        """Formats the data from the markets endpoint into a pandas dataframe."""

        # create dataframe without mentioning columns
        df = pd.DataFrame(data)

        # set the index to the id column
        df.set_index("id", inplace=True, drop=False)

        return df

    @staticmethod
    def market_chart_formatter(data: dict) -> pd.DataFrame:
        """Formats the data from the market_chart endpoint into a pandas dataframe."""

        # create a list to store the dataframes
        dfs = []

        # iterate through each key in the data dict
        for key in data.keys():
            # create a dataframe from the data
            df = pd.DataFrame(data[key], columns=["time", key])

            # set the index to the time column
            df.set_index("time", inplace=True)
            df.index = pd.to_datetime(df.index, unit="ms")

            # append the dataframe to the list
            dfs.append(df)

        # concatenate the dataframes and return
        return pd.concat(dfs, axis=1)

    @staticmethod
    def ohlc_formatter(data: dict) -> pd.DataFrame:
        """Formats the data from the ohlc endpoint into a pandas dataframe."""

        # create a dataframe from the data
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close"])

        # set the index to the time column
        df.set_index("time", inplace=True)
        df.index = pd.to_datetime(df.index, unit="ms")

        return df
