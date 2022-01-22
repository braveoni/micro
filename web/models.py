from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db, login_manager


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class Doors(db.Model):
    __tablename__ = 'doors'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(512), nullable=False)
    open = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    close = db.Column(db.DateTime)

    def __init__(self, location):
        self.location = location
        self.close = None

    @property
    def serialize(self):
        return {
            'id': self.id,
            'location': self.location,
            'open': self.open.strftime("%m/%d/%Y, %H:%M"),
            'close': self.close.strftime("%m/%d/%Y, %H:%M")
        }


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
