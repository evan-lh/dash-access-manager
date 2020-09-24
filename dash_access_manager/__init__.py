from .login import render_navbar_login, init_login_callbacks
from .logout import render_logout_button, init_logout_callbacks
from .signup import render_navbar_sign_up, init_signup_callbacks
from .models import User

from mongoengine import connect
from flask_login import LoginManager, current_user


def init_access_manager(app):
    init_login_callbacks(app)
    init_logout_callbacks(app)
    init_signup_callbacks(app)

    # Setup the LoginManager for the server
    login_manager = LoginManager()
    login_manager.init_app(app.server)
    login_manager.login_view = '/'

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

