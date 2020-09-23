import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from dash_access_manager.models import User

from flask_login import login_user


def render_navbar_login():
    return [
        html.Div(
            [
                dbc.Button("Login", id="login-open-button"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Login"),
                        dbc.ModalBody([
                            dcc.Location(id='login-url', refresh=True),
                            dbc.Form(
                                [
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Username", className="mr-2"),
                                            dbc.Input(
                                                id='login-username',
                                                type='text',
                                                placeholder='Enter your username'
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Password", className="mr-2"),
                                            dbc.Input(
                                                id='password-input',
                                                type='password',
                                                placeholder='Enter your password',
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                    dbc.Alert(
                                        "Sorry, the credentials are wrong...",
                                        id="alert-wrong-credentials",
                                        color="danger",
                                        fade=True,
                                        duration=4000,
                                        is_open=False,
                                    ),
                                    dbc.Alert(
                                        "Successfully login",
                                        id="alert-success-login",
                                        color="success",
                                        fade=True,
                                        duration=2000,
                                        is_open=False,
                                    ),
                                    dbc.Button(
                                        'Login',
                                        id='login-submit-button',
                                        n_clicks=0,
                                        color="primary"
                                    ),
                                ]
                            ),
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="login-close-button", className="ml-auto")
                        ),
                    ],
                    id="login-modal",
                ),
            ]
        )
    ]


def init_login_callbacks(app):
    @app.callback(
        Output("login-modal", "is_open"),
        [Input("login-open-button", "n_clicks"), Input("login-close-button", "n_clicks")],
        [State("login-modal", "is_open")],
    )
    def toggle_login_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        [Output('alert-success-login', 'is_open'),
         Output('alert-wrong-credentials', 'is_open')],
        [Input('login-submit-button', 'n_clicks')],
        [State('login-username', 'value'),
         State('password-input', 'value')])
    def perform_login(n_clicks, username, password):
        if n_clicks > 0:

            user = User.objects(username=username).first()

            if user:
                if user.check_password(password.encode('utf-8')):
                    login_user(user)
                    return True, False

            else:
                return False, True
        else:
            return False, False

    @app.callback(Output('login-url', 'pathname'),
                  [Input('alert-success-login', 'is_open')],
                  [State('login-url', 'pathname')])
    def refresh_page_on_login(is_open, pathname):

        if is_open:

            # Use the alternative home path to force the page to refresh

            if pathname == '/':
                return '/home'
            else:
                return '/'
        else:
            return pathname
