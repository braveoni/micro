import datetime
import json

from flask import jsonify, request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user
import pandas as pd

from .grapher import Graph

from . import app
from .forms import UserForm
from .manager import UserManager, DoorManager

u_manager = UserManager()
d_manager = DoorManager()


@app.route('/', methods=['GET'])
@login_required
def main():
    return render_template('main.html')


@app.route('/data')
@login_required
def get():
    g = Graph()
    freq = request.args.get('freq')

    line = g.get_line(freq) if freq else g.get_line()

    return jsonify({
        'doughnut': g.get_doughnut(),
        'line': line
    })


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        username, password = form.data['username'], form.data['password']
        if user := u_manager.check(username, password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Incorrect login or password')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/users', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        username, password = form.data['username'], form.data['password']
        if u_manager.get(username=username):
            flash('Such user already exist')
        else:
            u_manager.add(username, password)
            return redirect(url_for('create_user'))

    return render_template('create_user.html', form=form)


@app.route('/getdata')
def get_data():
    loc = request.args.get('loc')
    action = request.args.get('status')

    if action == '1':
        d_manager.add(loc)
    else:
        if not d_manager.get_data(location=loc, close=None):
            return "", 400

        d_manager.update(loc)

    return "", 200


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response
