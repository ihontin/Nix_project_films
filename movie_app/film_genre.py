"""Association table between two classes film_genre"""
from app import db

film_genre = db.Table('film_genre',
                      db.Column('film_genre_id', db.Integer, db.ForeignKey('film.film_id'), primary_key=True),
                      db.Column('genre_film_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
                      )
