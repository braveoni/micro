from werkzeug.security import check_password_hash

from .models import Users


def check_login(username, password):
    if username and password:
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return user

    return False
