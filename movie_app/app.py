"""Creation of the database"""
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'DEV'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:postgres_password@0.0.0.0:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
login_manager = LoginManager(app)
login_manager.init_app(app)
api = Api(app)

db = SQLAlchemy(app)


