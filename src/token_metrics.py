import math
import pandas as pd


class TokenMetrics(object):
    def __init__(self, csv_url_token_data):
        self.csv_url_token_data = csv_url_token_data
        self.process()

    def filter(self):
        self.tokens_df = self.tokens_df.drop(self.tokens_df.columns[0], axis=1)[1:]
        self.tokens_df["timestamp"] = pd.to_datetime(self.tokens_df["timestamp"], unit="s")

    def get_market_cap(self):
        self.market_cap_df = self.select_columns(
        self.tokens_df, ["timestamp", "supply", "market_price"]
        )
        self.market_cap_df["market_cap"] = self.market_cap_df.apply(
            lambda row: row.market_price * row.supply, axis=1
        )
        self.market_cap_df = self.select_columns(
            self.market_cap_df, ["timestamp", "market_cap"]
        )

    def get_staking_percentage(self):
        self.percent_staked_df = self.select_columns(
            self.tokens_df, ["timestamp", "supply", "staked"]
        )
        self.percent_staked_df["percent_staked"] = self.percent_staked_df.apply(
            lambda row: row.staked / row.supply, axis=1
        )
        self.percent_staked_df = self.select_columns(
            self.percent_staked_df, ["timestamp", "percent_staked"]
        )

    def get_supply_growth(self):
        self.supply_growth_df = self.select_columns(self.tokens_df, ["timestamp", "supply"])
        self.supply_growth_df["supply"] = self.supply_growth_df["supply"].apply(
            lambda x: ((float(x) - 30000) / 30000) * 100
        )
        self.supply_growth_df.columns = ["timestamp", "growth_rate"]

    def get_dilution(self):
        self.dilution_df = self.select_columns(
            self.supply_growth_df, ["timestamp", "growth_rate"]
        )
        self.dilution_df["growth_rate"] = (
            self.dilution_df["growth_rate"] / self.tokens_df["index"]
        )
        self.dilution_df.columns = ["timestamp", "dilution"]
    
    def get_apy(self):
        self.apy_df = self.select_columns(
            self.tokens_df, ["timestamp", "distribute"]
        )
        self.apy_df["distribute"] = (
            self.apy_df["distribute"] / self.tokens_df["staked"]
        )
        self.apy_df["distribute"] = (
            self.apy_df["distribute"].apply(lambda x: (math.pow(1 + x, 365 * 3) - 1) * 100)
        )
        self.apy_df.columns = ["timestamp", "apy"]

    def get_snapshot_metrics(self):
        self.last_df = self.tokens_df.sort_values("timestamp").tail(1)
        self.index = float(self.last_df["index"])
        self.price = float(self.last_df["market_price"])
        self.supply = float(self.last_df["supply"])

        self.tvl = float(self.price) * float(self.supply) * float(self.percent_staked_df.sort_values("timestamp").tail(1)['percent_staked'])
        self.reward = float(self.last_df["distribute"])
        self.rebase = self.reward / float(self.last_df["staked"])
        self.five_day_roi =  (math.pow(1 + self.rebase, 5 * 3) - 1) * 100
        self.apy = (math.pow(1 + self.rebase, 365 * 3) - 1) * 100

    def process(self):
        self.tokens_df = pd.read_csv(self.csv_url_token_data)

        self.filter()

        self.get_market_cap()
        self.get_staking_percentage()
        self.get_supply_growth()
        self.get_dilution()
        self.get_apy()
        self.get_snapshot_metrics()

    def fetch_data(self):
        self.process()
    
    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame