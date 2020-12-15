from .login import init_login_callbacks
from .logout import init_logout_callbacks
from .signup import init_sign_up_callbacks

from flask_login import LoginManager, current_user


class AccessManager:

    def __init__(self, app=None, user_class=None):
        if app is not None and user_class is not None:
            self.init_app(app, user_class)

    def init_app(self, app, user_class):
        init_login_callbacks(app, user_class)
        init_logout_callbacks(app)
        init_sign_up_callbacks(app, user_class)

        # Setup the LoginManager for the server
        login_manager = LoginManager()
        login_manager.init_app(app.server)
        login_manager.login_view = '/'

        # callback to reload the user object
        @login_manager.user_loader
        def load_user(user_id):
            return user_class.load_user(user_id)

    def is_authenticated(self):
        return current_user.is_authenticated
