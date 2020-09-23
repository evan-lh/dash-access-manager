import dash

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

import os

import dash_access_manager as dam


#####
#### Initialize the dash app
#####

external_stylesheets = [dbc.themes.LITERA]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

server.secret_key = os.urandom(12)

# Initiate access manager callbacks

dam.init_access_manager(app)

app.config.suppress_callback_exceptions = True

############
########### Set up the layout
############

app.layout = html.Div(children=[dcc.Location(id='url', refresh=False),
                                html.Div(id='root'),
                                html.Div(id='container')
                                ])


def render_default_page(navbar_button=[], page_content=[html.H3("Login successfull")]):
    return [
               dbc.Navbar([
                              dbc.NavbarBrand("Navbar"),
                          ] + navbar_button,
                          color="primary")
           ] + page_content


############
########### Define the callbacks
############

@app.callback(Output('root', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if dam.current_user.is_authenticated:
        return render_default_page(dam.render_logout_button(), dam.render_logged_page())
    else:
        return render_default_page(dam.render_navbar_login() + dam.render_navbar_sign_up(), dam.render_login_page())


if __name__ == "__main__":
    dam.connect(
        db='DatabaseName',
        host='DatabaseURL'
    )
    app.run_server()
