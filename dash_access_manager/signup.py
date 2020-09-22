import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from dash_access_manager.models import User

from flask_login import login_user

import bcrypt


def render_navbar_sign_up():
    return [
        html.Div(
            [
                dbc.Button("Sign up", id="sign-up-open-button"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Sign up"),
                        dbc.ModalBody([
                            dcc.Location(id='sign-up-url', refresh=True),
                            dbc.Form(
                                [
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Username", className="mr-2"),
                                            dbc.Input(
                                                id='sign-up-username',
                                                type='text',
                                                placeholder='Enter your username'
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                    dbc.Alert(
                                        "Sorry, this username is already used",
                                        id="alert-wrong-username",
                                        color="danger",
                                        fade=True,
                                        duration=4000,
                                        is_open=False,
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Password", className="mr-2"),
                                            dbc.Input(
                                                id='sign-up-password',
                                                type='password',
                                                placeholder='Enter your password',
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Confirm password", className="mr-2"),
                                            dbc.Input(
                                                id='sign-up-confirm-password',
                                                type='password',
                                                placeholder='Confirm your password',
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                    dbc.Alert(
                                        "Sorry, the passwords do not match",
                                        id="alert-wrong-password",
                                        color="danger",
                                        fade=True,
                                        duration=4000,
                                        is_open=False,
                                    ),
                                    dbc.Alert(
                                        "Successfully sign up",
                                        id="alert-success-sign-up",
                                        color="success",
                                        fade=True,
                                        duration=2000,
                                        is_open=False,
                                    ),
                                    dbc.Button(
                                        'Sign up',
                                        id='sign-up-submit-button',
                                        n_clicks=0,
                                        color="primary"
                                    ),
                                ]
                            )
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="sign-up-close-button", className="ml-auto")
                        ),
                    ],
                    id="sign-up-modal",
                ),
            ]
        )
    ]


def init_signup_callbacks(app):
    @app.callback(
        Output("sign-up-modal", "is_open"),
        [Input("sign-up-open-button", "n_clicks"), Input("sign-up-close-button", "n_clicks")],
        [State("sign-up-modal", "is_open")],
    )
    def toggle_sign_up_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        [Output('alert-success-sign-up', 'is_open'),
         Output('alert-wrong-username', 'is_open'),
         Output('alert-wrong-password', 'is_open')],
        [Input('sign-up-submit-button', 'n_clicks')],
        [State('sign-up-username', 'value'),
         State('sign-up-password', 'value'),
         State('sign-up-confirm-password', 'value')])
    def perform_sign_up(n_clicks, username, new_password, confirm_password):
        if n_clicks is not None and n_clicks > 0:

            user = User.objects(username=username).first()

            is_passwords_matched = new_password == confirm_password

            # Existing user with the username
            if user:
                return False, True, not is_passwords_matched

            else:
                if is_passwords_matched:
                    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    new_user = User(username=username, hashed_password=new_hashed_password)
                    new_user.save()

                    login_user(new_user)

                    return True, False, not is_passwords_matched

                return False, False, not is_passwords_matched
        else:
            return False, False, False

    @app.callback(Output('sign-up-url', 'pathname'),
                  [Input('alert-success-sign-up', 'is_open')],
                  [State('sign-up-url', 'pathname')])
    def refresh_page_on_sign_up(is_open, pathname):
        if is_open:

            # Use the alternative home path to force the page to refresh

            if pathname == '/':
                return '/home'
            else:
                return '/'
        else:
            return pathname
