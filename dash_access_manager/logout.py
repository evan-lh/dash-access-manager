import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from flask_login import logout_user

import dash_bootstrap_components as dbc


def render_logout_button():
    return [
        html.Div(
            [
                dbc.Button("Logout", id="logout-button"),
                dcc.Location(id='logout-url', refresh=True)
            ]
        )
    ]


def init_logout_callbacks(app):
    @app.callback(Output('logout-url', 'pathname'),
                  [Input('logout-button', 'n_clicks')],
                  [State('logout-url', 'pathname')])
    def perform_logout(n_clicks, pathname):
        if n_clicks is not None and n_clicks > 0:
            logout_user()

            # Use the alternative home path to force the page to refresh
            if pathname == '/':
                return '/home'
            else:
                return '/'
        else:
            return pathname
