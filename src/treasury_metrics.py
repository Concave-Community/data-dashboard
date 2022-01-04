import math
import pandas as pd


class TreasuryMetrics(object):
    def __init__(self, csv_url_treasury_data):
        self.csv_url_treasury_data = csv_url_treasury_data
        self.process()

    def process(self):
        self.treasury_df = pd.read_csv(self.csv_url_treasury_data)
        
    def fetch_data(self):
        self.process()

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame
