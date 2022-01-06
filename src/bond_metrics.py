import math
import pandas as pd


class BondMetrics(object):
    def __init__(self, csv_url_bond_data):
        self.csv_url_bond_data = csv_url_bond_data
        self.process()
    
    def filter(self):
        self.bonds_df["timestamp"] = pd.to_datetime(self.bonds_df["timestamp"], unit="s")

    def get_bcv(self):
        pass

    def process(self):
        self.bonds_df = pd.read_csv(self.csv_url_bond_data)
        self.filter()

        #TODO: Implement logic to iterate through multiple bonds
        #self.get_bcv()

    def fetch_data(self):
        self.process()

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame