from flask import request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from .models import Users
from . import app


@app.route('/main', methods=['GET'])
@login_required
def main():
    return f'Hello, {current_user.username}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Fill login and password')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)

    return response
