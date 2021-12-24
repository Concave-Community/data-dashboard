import pandas as pd
import math
import plotly.express as px

from dash import dcc, html
import dash_bootstrap_components as dbc


class Protocol(object):
    def __init__(self):
        self.df = pd.read_csv(self.csv_url)
        self.df = self.df.drop(self.df.columns[0], axis=1)[1:]
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="s")

    def preprocess(self):
        self.supply_growth_df = self.select_columns(self.df, ["timestamp", "supply"])
        self.supply_growth_df["supply"] = self.supply_growth_df["supply"].apply(
            lambda x: ((float(x) - 30000) / 30000) * 100
        )
        self.supply_growth_df.columns = ["timestamp", "growth-rate"]

        self.dilution_df = self.select_columns(
            self.supply_growth_df, ["timestamp", "growth-rate"]
        )
        self.dilution_df["growth-rate"] = (
            self.dilution_df["growth-rate"] / self.df["index"]
        )
        self.dilution_df.columns = ["timestamp", "dilution"]

        self.market_cap_df = self.select_columns(
            self.df, ["timestamp", "supply", "market_price"]
        )
        self.market_cap_df["market_cap"] = self.market_cap_df.apply(
            lambda row: row.market_price * row.supply, axis=1
        )
        self.market_cap_df = self.select_columns(
            self.market_cap_df, ["timestamp", "market_cap"]
        )

        self.percent_staked_df = self.select_columns(
            self.df, ["timestamp", "supply", "staked"]
        )
        self.percent_staked_df["percent_staked"] = self.percent_staked_df.apply(
            lambda row: row.staked / row.supply, axis=1
        )
        self.percent_staked_df = self.select_columns(
            self.percent_staked_df, ["timestamp", "percent_staked"]
        )

        self.last_df = self.df.sort_values("timestamp").tail(1)
        self.index = float(self.last_df["index"])
        self.price = float(self.last_df["market_price"])
        self.supply = float(self.last_df["supply"])

        self.reward = float(self.last_df["distribute"])
        self.rebase = self.reward / float(self.last_df["staked"])
        self.five_day_roi =  (math.pow(1 + self.rebase, 5 * 3) - 1) * 100
        self.apy = (math.pow(1 + self.rebase, 365 * 3) - 1) * 100

    @staticmethod
    def select_columns(data_frame, column_names):
        new_frame = data_frame.loc[:, column_names]
        return new_frame

    def charts(self):
        index_fig = px.line(self.df, x="timestamp", y="index", title="Index")

        market_cap_fig = px.line(
            self.market_cap_df,
            x="timestamp",
            y="market_cap",
            title="Market Cap",
        )

        percent_staked_fig = px.line(
            self.percent_staked_df,
            x="timestamp",
            y="percent_staked",
            title="Percentage Staked",
        )

        supply_growth_fig = px.line(
            self.supply_growth_df,
            x="timestamp",
            y="growth-rate",
            title="Supply Growth",
        )
        dilution_fig = px.line(
            self.dilution_df, x="timestamp", y="dilution", title="% Dilution"
        )
        output = html.Div(
            children=[
                html.Div(
                    [
                        html.H2(
                            children=[
                                f"{self.name} Dashboard",
                            ],
                            style={"text-align": "center"},
                        ),
                    ]
                ),
                html.Br(),
                html.Div(
                    children=[
                        dbc.Container(
                            children=[
                                dbc.Row(),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            self.get_card(
                                                "Market Cap",
                                                self.supply * self.price
                                            )
                                        ),
                                        dbc.Col(
                                            self.get_card("Price", self.price)
                                        ),
                                        dbc.Col(
                                            self.get_card("Index", self.index)
                                        ),
                                        dbc.Col(
                                            self.get_card(
                                                "Circulating Supply", self.supply
                                            )
                                        ),
                                    ]
                                ),
                                dbc.Row(),
                            ]
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    children=[
                        dbc.Container(
                            children=[
                                dbc.Row(),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            dcc.Graph(
                                                id="market_cap",
                                                figure=market_cap_fig,
                                            )
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="percent_staked",
                                                figure=percent_staked_fig,
                                            )
                                        ),
                                    ]
                                ),
                                dbc.Row(),
                            ], className="align-items-center d-flex justify-content-center"
                        )
                    ]
                ),
                html.Br(),
                html.Div(
                    children=[
                        dbc.Container(
                            children=[
                                dbc.Row(),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            self.get_card("Rebase", self.rebase)
                                        ),
                                        dbc.Col(
                                            self.get_card("Rebase ROI (5-day)", self.five_day_roi)
                                        ),
                                        dbc.Col(
                                            self.get_card("APY", self.apy)
                                        ),
                                    ]
                                ),
                                dbc.Row(),
                            ]
                        )
                    ]
                ),
                html.Br(),
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
        )
        return output

    @staticmethod
    def get_card(title, value):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6(
                        title,
                        className="align-items-center d-flex justify-content-center",
                    ),
                    html.P(
                        '{0:.2f}'.format(value),
                        className="align-items-center d-flex justify-content-center",
                    ),
                ]
            ),
            outline=True,
            color="success",
        )

        return card
