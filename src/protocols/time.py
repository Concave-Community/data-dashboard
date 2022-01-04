from ..protocol import Protocol
from ..bond_metrics import BondMetrics
from ..token_metrics import TokenMetrics
from ..treasury_metrics import TreasuryMetrics


class Time(Protocol):
    def __init__(self):
        self.name = "TIME"
        self.csv_url_bond_data = "https://raw.githubusercontent.com/Concave-Community/ohm-fork-data/main/data/wonderland/wonderland_bond.csv"
        self.csv_url_token_data = "https://raw.githubusercontent.com/Concave-Community/ohm-fork-data/main/data/wonderland/wonderland_fork.csv"
        self.csv_url_treasury_data = "https://raw.githubusercontent.com/Concave-Community/ohm-fork-data/main/data/wonderland/wonderland_treasury.csv"
        
        #self.bond_metrics = BondMetrics(self.csv_url_bond_data)
        self.token_metrics = TokenMetrics(self.csv_url_token_data)
        #self.treasury_metrics = TreasuryMetrics(self.csv_url_treasury_data)
        
        super(Time, self).__init__()
