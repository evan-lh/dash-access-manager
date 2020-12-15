from mongoengine import *
from flask_login import UserMixin
import bcrypt

class User(Document, UserMixin):
    username = StringField(required=True)
    hashed_password = StringField()

    def check_password(self, password: bytes) -> bool:
        return bcrypt.checkpw(password, self.hashed_password.encode('utf-8'))

    @staticmethod
    def create_user(username, password):
        new_hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, hashed_password=new_hashed_password)
        new_user.save()

        return new_user

    @staticmethod
    def load_user(user_id):
        return User.objects(id=user_id).first()
