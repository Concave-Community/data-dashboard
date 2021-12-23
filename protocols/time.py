import pandas as pd
import plotly.express as px

from dash import dcc, html


class Time(object):
    def __init__(self):
        self.name = "TIME"
        self.csv_url = "https://raw.githubusercontent.com/Concave-Community/ohm-fork-data/main/data/time.csv"
        self.time_df = pd.read_csv(self.csv_url)
        self.time_df = self.time_df.drop(self.time_df.columns[0], axis=1)[1:]
        self.time_df["timestamp"] = pd.to_datetime(self.time_df["timestamp"], unit="s")

    def preprocess(self):
        self.supply_growth_df = self.select_columns(
            self.time_df, ["timestamp", "supply"]
        )
        self.supply_growth_df["supply"] = self.supply_growth_df["supply"].apply(
            lambda x: ((float(x) - 30000) / 30000) * 100
        )
        self.supply_growth_df.columns = ["timestamp", "growth-rate"]

        self.dilution_df = self.select_columns(
            self.supply_growth_df, ["timestamp", "growth-rate"]
        )
        self.dilution_df["growth-rate"] = (
            self.dilution_df["growth-rate"] / self.time_df["index"]
        )
        self.dilution_df.columns = ["timestamp", "dilution"]

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame

    def charts(self):
        index_fig = px.line(self.time_df, x="timestamp", y="index", title="Index")
        supply_growth_fig = px.line(
            self.supply_growth_df,
            x="timestamp",
            y="growth-rate",
            title="Supply Growth (TIME)",
        )
        dilution_fig = px.line(
            self.dilution_df, x="timestamp", y="dilution", title="% Dilution (TIME)"
        )
        output = html.Div(
            children=[
                html.Div(
                    [
                        html.H2(
                            children=[
                                "Wonderland $TIME Dashboard",
                            ],
                            style={"text-align": "center"},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id="supply-growth",
                                            figure=supply_growth_fig,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="dilution", figure=dilution_fig),
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="index", figure=index_fig),
                                    ],
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
        return output
