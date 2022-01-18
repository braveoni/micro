from web import db
from web.models import Doors, Users
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class DoorManager:
    db = db

    def get_data(self, **kwargs):
        return self.db.session.query(Doors).filter_by(**kwargs).all()

    def add(self, loc):
        self.db.session.add(Doors(loc))
        self.db.session.commit()

    def update(self, loc):
        record = self.db.session.query(Doors).filter_by(location=loc, close=None).first()
        record.close = datetime.utcnow()
        db.session.commit()


class UserManager:
    db = db

    def get(self, **kwargs):
        return self.db.session.query(Users).filter_by(**kwargs).first()

    def add(self, username, password):
        self.db.session.add(Users(username=username, password=generate_password_hash(password)))
        self.db.session.commit()

    def check(self, username, password):
        if username and password:
            user = self.get(username=username)

            if user and check_password_hash(user.password, password):
                return user

        return False
