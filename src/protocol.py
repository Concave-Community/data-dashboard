import math
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from dash import dcc, html


class Protocol(object):
    def __init__(self):
        pass

    def charts(self):
        index_fig = px.line(self.token_metrics.tokens_df, x="timestamp", y="index", title="Index")

        market_cap_fig = px.line(
            self.token_metrics.market_cap_df,
            x="timestamp",
            y="market_cap",
            title="Market Cap",
        )

        percent_staked_fig = px.line(
            self.token_metrics.percent_staked_df,
            x="timestamp",
            y="percent_staked",
            title="Percentage Staked",
        )

        supply_growth_fig = px.line(
            self.token_metrics.supply_growth_df,
            x="timestamp",
            y="growth-rate",
            title="Supply Growth",
        )
        dilution_fig = px.line(
            self.token_metrics.dilution_df, x="timestamp", y="dilution", title="% Dilution"
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
                                                self.token_metrics.supply * self.token_metrics.price
                                            )
                                        ),
                                        dbc.Col(
                                            self.get_card("Price", self.token_metrics.price)
                                        ),
                                        dbc.Col(
                                            self.get_card("Index", self.token_metrics.index)
                                        ),
                                        dbc.Col(
                                            self.get_card(
                                                "Circulating Supply", self.token_metrics.supply
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
                                            self.get_card("Rebase", self.token_metrics.rebase)
                                        ),
                                        dbc.Col(
                                            self.get_card("Rebase ROI (5-day)", self.token_metrics.five_day_roi)
                                        ),
                                        dbc.Col(
                                            self.get_card("APY", self.token_metrics.apy)
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
