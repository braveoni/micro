from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('web.config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)

from web import routes
