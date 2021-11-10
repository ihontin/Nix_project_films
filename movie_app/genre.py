"""Table Genre"""

from app import db


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(15), nullable=True)




