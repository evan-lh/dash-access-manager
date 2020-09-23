# Dash-Access-Manager

![Python package](https://github.com/evan-lh/dash-access-manager/workflows/Python%20Package/badge.svg)
![GitHub](https://img.shields.io/github/license/evan-lh/dash-access-manager)

Dash-Access-Manager provides user access management for [Dash](https://github.com/plotly/dash). 

It is based on [Flask-Login](https://github.com/maxcountryman/flask-login) to manage user session and 
on [MongoEngine](https://github.com/MongoEngine/mongoengine) to use MongoDB databases.

## Table of contents

  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Contributing](#contributing)
  * [Changelog](#changelog)
  * [License](#license)

## Description

This is an implementation of an access management to be used in a dash app. 
It provides login, logout and sign up buttons that can be integrated in a layout of a dash app.

## Installation

Install the extension with pip:

    pip install dash-access-manager

## Usage

Once installed, import the package in your `app.py`.

    import dash-access-manager as dam

    app = dash.Dash(__name__)
    
    server = app.server
    
    
Then, you have to set up the access manager. You __need to change__ `your_secret_key_here` as it not secret. 
To do so, you can generate a secret key with the `os` module by using `os.urandom(12)`

    #Define a secret key that is required for Flask-Login to manage user session
    server.secret_key = 'your_secret_key_here' 
    
    # Suppress errors for callbacks acting on layouts that are not displayed yet
    app.config.suppress_callback_exceptions = True

    # Initialize the acess manager
    dam.init_access_manager(app)
    
After this you will define the layouts and callbacks of your dash app. Here is an simple example that can be used as it is.
    
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
    
    
    @app.callback(Output('root', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if dam.current_user.is_authenticated:
            return render_default_page(dam.render_logout_button(), dam.render_logged_page())
        else:
            return render_default_page(dam.render_navbar_login() + dam.render_navbar_sign_up(), dam.render_login_page())
  
  
Finally, you need to connect the app with your MongoDB database before running your app. 
You have to change `DatabaseName` and `DatabaseURL` with the ones you want to use. 
If you want to use MongoDB you need to this change the `host` parameter at `mongodb+srv://username.password@cluster.url` 
where you have to replace `username`, `password` and `cluster.url` by your information.
   
    if __name__ == "__main__":
        dam.connect(
            db='DatabaseName',
            host='DatabaseURL'
        )
        app.run_server()
    
You can use this file [app.py] to try it out.

## Contributing
This project is under development so contributions are welcome to improve the code.
Have a look at [CONTRIBUTING].

## Changelog

Take a look at [CHANGELOG] for more details. 

## License

Distributed under the MIT License. See [LICENSE] for more information. 

[app.py]: https://github.com/evan-lh/dash-access-manager/blob/master/example/app.py
[CONTRIBUTING]: https://github.com/evan-lh/dash-access-manager/blob/master/docs/CONTRIBUTING.md
[CHANGELOG]: https://github.com/evan-lh/dash-access-manager/blob/master/docs/CHANGELOG.md
[LICENSE]: https://github.com/evan-lh/dash-access-manager/blob/master/LICENSE