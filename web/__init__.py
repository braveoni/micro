from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('web.config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from web import routes
