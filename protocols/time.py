from .protocol import Protocol


class Time(Protocol):
    def __init__(self):
        self.name = "TIME"
        self.csv_url = "https://raw.githubusercontent.com/Concave-Community/ohm-fork-data/main/data/time.csv"
        super(Time, self).__init__()
