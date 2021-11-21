"""Table Director"""

from app import db
from film_director import Filmdirector

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=True)
    fk_filmdir_id = db.relationship('Film', secondary='filmdirector',
                                 back_populates="fk_director_id")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
