"""Creation of the database"""
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'DEV'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://postgres:postgres_password@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
login_manager = LoginManager(app)
login_manager.init_app(app)
api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)


def create_db():
    """Create all models"""
    from film_genre import Filmgenre
    from film_director import Filmdirector
    from film import Film
    from user import User
    from genre import Genre
    from director import Director

    db.create_all()