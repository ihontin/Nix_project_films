"""Creation and filling database Films library"""
import json
from app import db

# import all models
from film_genre import Filmgenre
from film_director import Filmdirector
from film import Film
from user import User
from genre import Genre
from director import Director



def create_db():
    """Create all models"""
    from film_genre import Filmgenre
    from film_director import Filmdirector
    from film import Film
    from user import User
    from genre import Genre
    from director import Director

    db.create_all()



def seeding_db():
    """Seeding database"""
    result = db.session.query(Director).all()

    if len(result) == 0:
        directors_list, genre_list, film_list = [], [], []
        # Fill DIRECTOR Table
        with open("./data/director.json", 'r', encoding='utf-8') as dir_file:
            json_direct = json.load(dir_file)

        for row in json_direct:
            fill_direct = Director(first_name=row['first_name'], last_name=row['last_name'])
            directors_list.append(fill_direct)
            db.session.add(fill_direct)

        # Fill GENRE Table
        with open("./data/genre.json", 'r', encoding='utf-8') as gen_file:
            json_genre = json.load(gen_file)

        for row in json_genre:
            fill_genre = Genre(title=row['title'])
            genre_list.append(fill_genre)
            db.session.add(fill_genre)

        # Fill USER Table
        with open("./data/user.json", 'r', encoding='utf-8') as user_file:
            json_user = json.load(user_file)

        for row in json_user:
            fill_user = User(login=row['login'],
                             password=row['password'], admin=row['admin'])
            db.session.add(fill_user)

        # Fill FILM Table
        with open("./data/film.json", 'r', encoding='utf-8') as film_file:
            json_film = json.load(film_file)

        for row in json_film:
            fill_film = Film(title=row['title'],
                             release=row['release'], poster=row['poster'], rating=row['rating'],
                             description=row['description'], fk_user_id=row['fk_user_id'])
            film_list.append(fill_film)
            db.session.add(fill_film)

        # Fill FILM_director Table
        for i in range(len(film_list)):
            directors_list[i + 1].fk_filmdir_id.append(film_list[i])

        # Fill Filmgenre Table
        genre_list[0].fk_filmgen_id.append(film_list[0])
        genre_list[5].fk_filmgen_id.append(film_list[1])
        genre_list[0].fk_filmgen_id.append(film_list[1])
        genre_list[0].fk_filmgen_id.append(film_list[2])
        genre_list[1].fk_filmgen_id.append(film_list[3])
        genre_list[0].fk_filmgen_id.append(film_list[3])

        db.session.commit()
    else:
        print("The database is seeded")
        db.session.commit()
