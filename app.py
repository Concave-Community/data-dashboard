import dash
import dash_bootstrap_components as dbc

from dash import Input, Output, dcc, html
from src.protocols.time import Time

# load and pre-process protocol data
wonderland = Time()

# build Dash layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.A(
            html.Img(
                src="assets/concave-logo.jpeg",
                style={"float": "right", "height": "50px"},
            ),
        ),
        html.P("Concave Community", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("$TIME", href="/time", active="exact"),
                dbc.NavLink("WIP", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            [
                html.H2(
                    children=[
                        "Dashboards",
                    ],
                    style={"text-align": "center"},
                ),
            ]
        )
    elif pathname == "/time":
        return wonderland.charts()
    elif pathname == "/page-2":
        return html.Div(
            [
                html.H2(
                    children=[
                        "WIP Fork2 dashboard",
                    ],
                    style={"text-align": "center"},
                ),
            ]
        )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
