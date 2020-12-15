import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask_login import logout_user


def render_logout_button():
    """
    Render the logout button

    Returns
    -------
    list
        List of components to display
    """

    return [
        html.Div(
            [
                dbc.Button("Logout", id="logout-button", n_clicks=0),
                dcc.Location(id='logout-url', refresh=True)
            ]
        )
    ]


def init_logout_callbacks(app):
    """
    Define the callbacks used to perform the logout
    """

    @app.callback(Output('logout-url', 'pathname'),
                  [Input('logout-button', 'n_clicks')],
                  [State('logout-url', 'pathname')])
    def perform_logout(n_clicks, pathname):
        if n_clicks:
            logout_user()

            # Return the alternative home path to force the page to refresh
            if pathname == '/':
                return '/home'
            else:
                return '/'
        else:
            return pathname
