from flask import jsonify, request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user

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


@app.route('/moderate', methods=['GET', 'POST'])
def moderate():
    data = d_manager.get_data()

    return render_template('moderate.html', data=data)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        delete = request.form.get('delete')
        field = request.form.get('field')
        value = request.form.get('value')
        editid = request.form.get('id')

        if delete:
            d_manager.delete(id=editid)
        else:
            if field == 'location':
                record = d_manager.update_data(id=editid)
                record.location = value
            if field == 'open':
                record = d_manager.update_data(id=editid)
                record.open = value
            if field == 'close':
                record = d_manager.update_data(id=editid)
                record.close = value

            d_manager.commit()

        success = 1

    return jsonify(success)


@app.route('/table')
@login_required
def table():
    data = d_manager.get_data()

    return render_template('table.html', data=data)


@app.route('/data')
@login_required
def get():
    g = Graph()
    freq = request.args.get('freq')

    line = g.get_line(freq) if freq else g.get_line()

    return jsonify({
        'doughnut': g.get_doughnut(),
        'line': line,
        'table': g.get_table()
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
    elif not d_manager.get_data(location=loc, close=None):
        return "", 400

    d_manager.update(loc)

    return "", 200


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response
