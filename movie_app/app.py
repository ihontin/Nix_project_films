"""Creation of the database"""
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = 'Great secret'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:postgres_password@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
ma = Marshmallow(app)
db = SQLAlchemy(app)

api = Api(app)



def create_db():
    """Create all models"""
    from film_genre import film_genre
    from film_director import film_director
    from film import Film
    from user import User
    from genre import Genre
    from director import Director

    db.create_all()