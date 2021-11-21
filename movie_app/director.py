"""Table Director"""

from app import db


class Director(db.Model):
    director_id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=True)


