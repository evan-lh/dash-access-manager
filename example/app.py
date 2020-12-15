import dash

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

import os

import dash_access_manager as dam
from example.models import User

from mongoengine import connect

server_port = os.environ.get('PORT', 5000)
database_name = os.environ.get('DATABASE_NAME')
database_url = os.environ.get('DATABASE_URL')

#####
#### Initialize the dash app
#####

external_stylesheets = [dbc.themes.LITERA]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
server.secret_key = os.urandom(12)

app.config.suppress_callback_exceptions = True

# Initiate access manager callbacks

access_manager = dam.AccessManager(app, User)

connect(
    db=database_name,
    host=database_url
)

############
########### Set up the layout
############

app.layout = html.Div(children=[dcc.Location(id='url', refresh=False),
                                html.Div(id='root'),
                                html.Div(id='container')
                                ])


def render_default_page(navbar_button=[], page_content=[html.H3("Some content")]):
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
    if access_manager.is_authenticated():
        return render_default_page(dam.render_logout_button(), [html.H3('Logged in successfully')])
    else:
        return render_default_page(dam.render_navbar_login() + dam.render_navbar_sign_up(), [html.H3('Please log in to continue')])


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=5000)

