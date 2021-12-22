
import dash
import pandas as pd
import plotly.express as px

from dash import dcc
from dash import html

from protocols.time import Time
from utils.util import select_columns

# load and pre-process protocol data
wonderland = Time()
wonderland.preprocess()

# create figures
index_fig = px.line(wonderland.time_df, x="timestamp", y="index", title='Index')
supply_growth_fig = px.line(wonderland.supply_growth_df, x="timestamp", y="growth-rate", title='Supply Growth (TIME)')
dilution_fig = px.line(wonderland.dilution_df, x="timestamp", y="dilution", title='% Dilution (TIME)')

# build Dash layout
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children=[
                        "Policy Dashboard",
                        html.A(
                            html.Img(
                                src="assets/concave-logo.jpeg",
                                style={"float": "right", "height": "50px"},
                            ),
                            href="https://concavers.xyz",
                        ),
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
                                    id='supply-growth',
                                    figure=supply_growth_fig,
                                ),  
                            ],
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='dilution',
                                    figure=dilution_fig
                                ),
                            ],                    
                        ),
                    ]
                ),
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)