import math
import pandas as pd


class TreasuryMetrics(object):
    def __init__(self, csv_url_treasury_data, reserve_assets, lp_assets):
        self.csv_url_treasury_data = csv_url_treasury_data
        self.reserve_assets = reserve_assets
        self.lp_assets = lp_assets
        self.process()

    def filter(self):
        self.treasury_df["timestamp"] = pd.to_datetime(self.treasury_df["timestamp"], unit="s")

    def get_rfv(self):
        pass

    def get_total_liquidity(self):
        pass

    def get_treasury_market_value(self):
        self.treasury_df = self.treasury_df[self.treasury_df['name'].isin(self.reserve_assets)]
        self.treasury_market_value_df = self.treasury_df.groupby(['timestamp']).value.agg(['sum'])
        self.treasury_market_value_df['timestamp'] = self.treasury_df['timestamp'].unique()

    def process(self):
        self.treasury_df = pd.read_csv(self.csv_url_treasury_data)

        self.filter()

        self.get_treasury_market_value()
        
    def fetch_data(self):
        self.process()

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame
