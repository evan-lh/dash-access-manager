import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from flask_login import login_user


def render_navbar_sign_up():
    """
    Render a sign up button that open a form to sign up

    Returns
    -------
    list
        List of components to display
    """

    # Define the username input used to sign up
    username_signup_login = dbc.FormGroup(
        [
            dbc.Label("Username", className="mr-2"),
            dbc.Input(
                id='sign-up-username',
                type='text',
                placeholder='Enter your username'
            ),
            dbc.FormFeedback(
                "This username is valid", valid=True
            ),
            dbc.FormFeedback(
                "This username is not valid",
                valid=False,
            )
        ],
        className="mr-3",
    )

    # Define the password input used to sign up
    password_signup_input = dbc.FormGroup(
        [
            dbc.Label("Password", className="mr-2"),
            dbc.Input(
                id='sign-up-password',
                type='password',
                placeholder='Enter your password',
            ),
            dbc.FormFeedback(
                "This password is valid", valid=True
            ),
            dbc.FormFeedback(
                "This password is not valid",
                valid=False,
            )
        ],
        className="mr-3",
    )

    # Define the confirm password input used to sign up
    confirm_password_signup_input = dbc.FormGroup(
        [
            dbc.Label("Confirm password", className="mr-2"),
            dbc.Input(
                id='sign-up-confirm-password',
                type='password',
                placeholder='Confirm your password',
            ),
            dbc.FormFeedback(
                "This password is valid", valid=True
            ),
            dbc.FormFeedback(
                "This password is not the same ",
                valid=False,
            )
        ],
        className="mr-3",
    )

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
                                    username_signup_login,
                                    password_signup_input,
                                    confirm_password_signup_input,
                                    dbc.Alert(
                                        "Sorry, at least one input is wrong...",
                                        id="alert-wrong-sign-up",
                                        color="danger",
                                        fade=True,
                                        dismissable=True,
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


def init_sign_up_callbacks(app, User):
    """
    Define the callbacks used to perform the sign up
    """

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
        [Output("sign-up-username", "valid"), Output("sign-up-username", "invalid")],
        [Input("sign-up-username", "value")],
    )
    def check_username_validity(username):
        if username:
            if len(username) > 1:  # Check the format of the username
                # If the format is good, check if the username is open
                user = User.objects(username=username).first()

                if user:
                    return False, True
                else:
                    return True, False
            else:
                return False, True
        return False, False

    @app.callback(
        [Output("sign-up-password", "valid"), Output("sign-up-password", "invalid")],
        [Input("sign-up-password", "value")],
    )
    def check_password_validity(password):
        if password:
            if len(password) >= 1:
                return True, False
            else:
                return False, True
        return False, False

    @app.callback(
        [Output("sign-up-confirm-password", "valid"), Output("sign-up-confirm-password", "invalid")],
        [Input("sign-up-confirm-password", "value"), Input("sign-up-password", "value")]
    )
    def check_confirm_password_validity(confirm_password, password):
        if confirm_password and password:
            if confirm_password == password:
                return True, False
            else:
                return False, True
        return False, False

    @app.callback(
        [Output('alert-success-sign-up', 'is_open'),
         Output('alert-wrong-sign-up', 'is_open')],
        [Input('sign-up-submit-button', 'n_clicks')],
        [State('sign-up-username', 'value'),
         State('sign-up-password', 'value'),
         State('sign-up-confirm-password', 'value')])
    def perform_sign_up(n_clicks, username, new_password, confirm_password):
        if n_clicks:

            if username and new_password and confirm_password:

                user = User.objects(username=username).first()

                is_passwords_matched = new_password == confirm_password

                # Existing user with the username
                if user:
                    return False, True

                else:
                    if is_passwords_matched:
                        new_user = User.create_user(username=username, password=new_password)
                        login_user(new_user)

                        return True, False

                    return False, True
            else:
                return False, True
        else:
            return False, False

    @app.callback(Output('sign-up-url', 'pathname'),
                  [Input('alert-success-sign-up', 'is_open')],
                  [State('sign-up-url', 'pathname')])
    def refresh_page_on_sign_up(is_open, pathname):
        if is_open:

            # Return the alternative home path to force the page to refresh
            if pathname == '/':
                return '/home'
            else:
                return '/'
        else:
            return pathname
