import math
import pandas as pd


class TreasuryMetrics(object):
    def __init__(self, csv_url_treasury_data):
        self.csv_url_treasury_data = csv_url_treasury_data
        self.process()

    def process(self):
        self.treasury_df = pd.read_csv(self.csv_url_treasury_data)
        self.treasury_df = self.treasury_df.drop(self.treasury_df.columns[0], axis=1)[1:]
        self.treasury_df["timestamp"] = pd.to_datetime(self.treasury_df["timestamp"], unit="s")
        self.supply_growth_df = self.select_columns(self.treasury_df, ["timestamp", "supply"])
        self.supply_growth_df["supply"] = self.supply_growth_df["supply"].apply(
            lambda x: ((float(x) - 30000) / 30000) * 100
        )
        self.supply_growth_df.columns = ["timestamp", "growth-rate"]

        self.dilution_df = self.select_columns(
            self.supply_growth_df, ["timestamp", "growth-rate"]
        )
        self.dilution_df["growth-rate"] = (
            self.dilution_df["growth-rate"] / self.fork_df["index"]
        )
        self.dilution_df.columns = ["timestamp", "dilution"]

        self.market_cap_df = self.select_columns(
            self.treasury_df, ["timestamp", "supply", "market_price"]
        )
        self.market_cap_df["market_cap"] = self.market_cap_df.apply(
            lambda row: row.market_price * row.supply, axis=1
        )
        self.market_cap_df = self.select_columns(
            self.market_cap_df, ["timestamp", "market_cap"]
        )

        self.percent_staked_df = self.select_columns(
            self.treasury_df, ["timestamp", "supply", "staked"]
        )
        self.percent_staked_df["percent_staked"] = self.percent_staked_df.apply(
            lambda row: row.staked / row.supply, axis=1
        )
        self.percent_staked_df = self.select_columns(
            self.percent_staked_df, ["timestamp", "percent_staked"]
        )

        self.last_df = self.treasury_df.sort_values("timestamp").tail(1)
        self.index = float(self.last_df["index"])
        self.price = float(self.last_df["market_price"])
        self.supply = float(self.last_df["supply"])

        self.reward = float(self.last_df["distribute"])
        self.rebase = self.reward / float(self.last_df["staked"])
        self.five_day_roi =  (math.pow(1 + self.rebase, 5 * 3) - 1) * 100
        self.apy = (math.pow(1 + self.rebase, 365 * 3) - 1) * 100

    def fetch_data(self):
        self.process()

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame
