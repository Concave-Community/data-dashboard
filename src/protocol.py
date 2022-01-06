import math
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from dash import dcc, html


class Protocol(object):
    def __init__(self):
        self.template = 'seaborn'

    def charts(self):
        index_fig = px.line(self.token_metrics.tokens_df, 
            x="timestamp", 
            y="index", 
            title="Index",
            labels ={'timestamp':'Timestamp', 'index':'Index'},
            template=self.template
        )
        market_cap_fig = px.line(
            self.token_metrics.market_cap_df,
            x="timestamp",
            y="market_cap",
            title="Market Cap",
            labels ={'timestamp':'Timestamp', 'market_cap':'Market Cap'},
            template=self.template
        )
        percent_staked_fig = px.line(
            self.token_metrics.percent_staked_df,
            x="timestamp",
            y="percent_staked",
            title="Percentage Staked",
            labels ={'timestamp':'Timestamp', 'percent_staked':'Staked (%)'},
            template=self.template
        )
        supply_growth_fig = px.line(
            self.token_metrics.supply_growth_df,
            x="timestamp",
            y="growth_rate",
            title="Supply Growth",
            labels ={'timestamp':'Timestamp', 'growth_rate':'Growth Rate (%)'},
            template=self.template
        )
        dilution_fig = px.line(
            self.token_metrics.dilution_df, 
            x="timestamp", 
            y="dilution", 
            title="Dilution",
            labels ={'timestamp':'Timestamp', 'dilution':'Dilution Rate (%)'},
            template=self.template
        )
        apy_fig = px.line(
            self.token_metrics.apy_df, 
            x="timestamp", 
            y="apy", 
            title="APY",
            labels ={'timestamp':'Timestamp', 'apy':'APY (%)'},
            template=self.template
        )
        treasury_market_value_fig = px.line(
            self.treasury_metrics.treasury_market_value_df, 
            x="timestamp", 
            y="sum", 
            title="Treasury Market Value",
            labels ={'timestamp':'Timestamp', 'sum':'Value (USD)'},
            template=self.template
        )
        treasury_asset_breakdown_fig = px.bar(
            self.treasury_metrics.treasury_df, 
            x="timestamp", 
            y="value", 
            title="Treasury Asset Breakdown",
            labels ={'timestamp':'Timestamp', 'value':'Value (USD)'},
            template=self.template,
            color="name"
        )
        bcv_fig = px.line(
            self.bond_metrics.bonds_df, 
            x="timestamp", 
            y="control_variable", 
            title="MIM BCV",
            labels ={'timestamp':'Timestamp', 'control_variable':'Bond Control Variable'},
            template=self.template,
            color="target"
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
                                            self.get_card("Market Cap", self.token_metrics.supply * self.token_metrics.price, prefix='$')
                                        ),
                                        dbc.Col(
                                            self.get_card("Price", self.token_metrics.price, prefix='$')
                                        ),
                                        dbc.Col(
                                            self.get_card("Index", self.token_metrics.index)
                                        ),
                                        dbc.Col(
                                            self.get_card("Circulating Supply", self.token_metrics.supply
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
                                            self.get_card("Rebase", self.token_metrics.rebase, decimals='4')
                                        ),
                                        dbc.Col(
                                            self.get_card("Rebase ROI (5-day)", self.token_metrics.five_day_roi, suffix='%')
                                        ),
                                        dbc.Col(
                                            self.get_card("APY", self.token_metrics.apy, suffix='%')
                                        ),
                                        dbc.Col(
                                            self.get_card("TVL", self.token_metrics.tvl, prefix='$')
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
                                dcc.Graph(id="market_cap", figure=market_cap_fig,
                                ),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="percent_staked", figure=percent_staked_fig,
                                ),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),                        
                        html.Div(
                            children=[
                                dcc.Graph(id="supply-growth", figure=supply_growth_fig,
                                ),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="index", figure=index_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="apy", figure=apy_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="dilution", figure=dilution_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="treasury_market_value", figure=treasury_market_value_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="treasury_asset_breakdown", figure=treasury_asset_breakdown_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(id="bcv", figure=bcv_fig),
                            ],
                            style={'width': '50%', 'display': 'inline-block'},
                        ),
                    ]
                ),
            ]
        )
        return output

    @staticmethod
    def get_card(title, value, decimals='2', prefix='', suffix = ''):
        fmt = '{0:,.' + decimals + 'f}'
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6(
                        title,
                        className="align-items-center d-flex justify-content-center",
                    ),
                    html.P(
                        prefix + fmt.format(value) + suffix,
                        className="align-items-center d-flex justify-content-center",
                    ),
                ]
            ),
            outline=False,
            color="light",
        )
        return card
