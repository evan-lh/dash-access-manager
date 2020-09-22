from mongoengine import *
from flask_login import UserMixin
import bcrypt


class User(Document, UserMixin):
    username = StringField(required=True)
    hashed_password = StringField()

    def check_password(self, password: bytes) -> bool:
        return bcrypt.checkpw(password, self.hashed_password.encode('utf-8'))
