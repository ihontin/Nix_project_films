#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================

"""Creation of the database"""
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
print('7 app')
app = Flask(__name__)
app.secret_key = 'DEV'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:postgres_password@lokalhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
login_manager = LoginManager(app)
login_manager.init_app(app)
api = Api(app)

# manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from filmapp import models, routes
print('18 app')

