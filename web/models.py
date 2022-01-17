from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, unique=True)
    door_list = db.relationship('Doors', backref='locations', lazy='dynamic')


class Doors(db.Model):
    __tablename__ = 'doors'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(512), db.ForeignKey('locations.name'), nullable=False)
    action = db.relationship('Actions', backref='doors', lazy='dynamic')


class Actions(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow())
    door_id = db.Column(db.Integer, db.ForeignKey('doors.id'))
    action = db.Column(db.Boolean, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
