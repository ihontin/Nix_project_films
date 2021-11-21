"""Start module"""
from flask_migrate import Migrate
from flask_script import Manager

from app import app, db
import routes

manager = Manager(app)
migrate = Migrate(app, db)

from film_genre import film_genre
from film_director import film_director
from film import Film
from user import User
from genre import Genre
from director import Director


@manager.command
def creation():
    """Database creation"""
    from app import create_db
    create_db()


@manager.command
def seeding():
    """Seeding database"""
    from manage import seeding_db
    seeding_db()


# python main.py runserver  --host=127.0.0.2 --port 8000

# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade



if __name__ == "__main__":
    app.run(debug=True)
    # manager.run()
