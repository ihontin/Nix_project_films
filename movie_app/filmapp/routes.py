"""Routes and function to all models"""
import datetime

from flask import abort
from flask_restx import Resource, reqparse
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from filmapp import db, api, login_manager
# from film_genre import Filmgenre
from filmapp.film_director import Filmdirector
from filmapp.film import Film
from filmapp.user import User
from filmapp.genre import Genre
from filmapp.director import Director
from filmapp.models import model_user, model_login, model_add, model_del_director, model_film
from logs.logs import film_log
print('18 routes')


@api.route('/')
class RootPage(Resource):
    """Root page"""

    # @api.doc(body=user_login_resource)
    @api.marshal_with(model_user, code=200)
    def get(self):
        """Greeting"""
        return {'Hello': 'World'}


@login_manager.user_loader
def load_user(user_id):
    """ User in session """
    return db.session.query(User).get(user_id)


@api.route('/login')
class LogPage(Resource):
    """User login"""

    @api.marshal_with(model_login, code=200)
    @api.doc("User authorization.")
    def post(self):
        """Post login method"""
        # if current_user.is_active:
        #     abort(403, "User already login")
        parser = reqparse.RequestParser()
        parser.add_argument('nick', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        # user_log = db.session.query(User).filter(User.login == args['nick']).first()
        print(args['nick'])
        user_log = User.query.filter(User.login == args['nick']).first()
        print(user_log)
        user_pass = False
        if user_log:
            user_pass = check_password_hash(user_log.password, str(args['password']))
        if user_pass:
            login_user(user_log)
            user_id = current_user.id
            film_log.save_logs(f"User id: {user_id} logged in")
            return {
                'id': user_id,
                'login': True}
        abort(403, "Nickname or password not correct")


@api.route('/logout')
class LogoutPage(Resource):
    """Post method for login"""

    @api.marshal_with(model_login, code=200)
    @login_required
    @api.doc("User logout.")
    def post(self):
        """Logout user"""
        user_id = current_user.id
        logout_user()
        film_log.save_logs(f"User id: {user_id} Logout")
        return {'id': user_id, 'login': False}


# @app.after_request
# def redirect_to_signin(response):
#     """Redirect to LogPage"""
#     if response.status_code == 401:
#         return redirect(url_for('log_page'))
#     return response


@api.route('/register/')
class Register(Resource):
    """User registration"""

    @api.marshal_with(model_user, code=200)
    @api.doc("User registration.")
    def post(self):
        """Add new user"""
        if current_user.is_active:
            abort(403, description="Logout first")
        parser = reqparse.RequestParser()
        parser.add_argument('nick', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('password2', type=str, required=True)
        args = parser.parse_args()
        exist_nick = db.session.query(User).filter(User.login == args['nick']).first()
        if exist_nick:
            abort(403, f"User with nickname {args['nick']} already exists. Login should be unique")
        if not (args['nick'] and args['password'] and args['password2']):
            abort(403, description="All fields must be filled")
        if args['password'] != args['password2']:
            abort(406, description="Passwords should be equal")
        if len(args['nick']) <= 4 or len(args['password']) <= 4:
            abort(406, description="Passwords and nick should be at least five characters long")
        elif len(args['nick']) > 4 and len(args['password']) > 4:
            pass_hash = generate_password_hash(args['password'])
            new_user = User(login=args['nick'], password=pass_hash, admin=0)
            db.session.add(new_user)
            db.session.commit()
            if new_user:
                film_log.save_logs(f"User id: {new_user.id} registered")
                return {"register": True}

        return abort(403, "Nickname or password not correct")


def film_sort_def(operation, pagin):
    """Sorting films"""
    if operation == 'rating':
        var = db.session.query(Film).order_by(Film.rating).paginate(page=pagin).items
        return var
    elif operation == 'release':
        var = db.session.query(Film).order_by(Film.release).paginate(page=pagin).items
        return var
    var = db.session.query(Film).order_by(Film.title).paginate(page=pagin).items
    return var


@api.route('/films-api/Sort-Searc')
class SortFilms(Resource):
    """Sorting films by: release, rating and by_title by default"""

    @api.marshal_with(model_film, code=200)
    @api.doc("Sorting films by release, rating and by_title by default.")
    def get(self):
        print('145 routes')
        """Choose operation and sorting films"""
        parser = reqparse.RequestParser()
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('operation', type=str, default='by_title')
        args = parser.parse_args()
        res = film_sort_def(args['operation'], args['pagination'])
        if current_user.is_active:
            film_log.save_logs(f"User id: {current_user.id};"
                               f" operation: {args['operation']}; "
                               f" class SortFilms")
        return res


def search_by_operation(text, operation, pagin, lower_year, upper_year):
    """serching films"""
    if operation == 'none':
        return "Len should be more then 1 symbol", 400
    elif operation == 'director':
        if search_empty_fields(text):
            search = "%{}%".format(text)
            search_last_name = Film.query.join(Film.fk_director_id). \
                filter(Director.last_name.like(search)).paginate(page=pagin).items
            if search_last_name:
                return search_last_name
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'genre':
        if search_empty_fields(text):
            search_genre = Film.query.join(Film.fk_genre_id). \
                filter(Genre.title.like(text)).paginate(page=pagin).items
            if search_genre:
                return search_genre
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    elif operation == 'relisedate':
        search_relisedate = Film.query.filter(
            Film.release > lower_year + '-01-01',
            Film.release < upper_year + '-12-31').paginate(page=pagin).items
        if search_relisedate:
            return search_relisedate
        return "Films not found", 404


def search_empty_fields(text):
    """If fields are empty, return - 404"""
    if len(text) == 0:
        return False
    elif len(text) < 2:
        return False
    return True


@api.route('/films-api/Searc')
class SearchFilms(Resource):
    """Search by: genre, director, relisedate"""

    @api.marshal_with(model_film, code=200)
    @api.doc("Search by genre, director or relise date.")
    def get(self):
        """Choose operation and searching films"""
        upper_year = str(datetime.datetime.now().year)
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, default='none')
        parser.add_argument('operation', type=str, default='none')
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('lower_year', type=str, default='1900')
        parser.add_argument('upper_year', type=str, default=upper_year)
        args = parser.parse_args()
        res = search_by_operation(args['text'], args['operation'],
                                  args['pagination'], args['lower_year'], args['upper_year'])
        if current_user.is_active:
            film_log.save_logs(f"User id: {current_user.id};"
                               f" operation: {args['operation']}; "
                               f" class SearchFilms")
        else:
            film_log.save_logs(f"User anonymous;"
                               f" operation: {args['operation']}; "
                               f" class SearchFilms")
        return {"Films": res}


def chosen_sort(chosen):
    """Choose kind of sorting for search"""
    sort_var = Film.title
    if chosen == "rating":
        sort_var = Film.rating
    elif chosen == "release":
        sort_var = Film.release
    return sort_var


def search_operation_sort_rating(text, operation, ascending,
                                 pagin, lower_year, upper_year, sorting_by):
    """Serching films, sort by rating
    descending by defoult"""
    sort_variable = chosen_sort(sorting_by)
    if operation == 'none':
        return "Len should be more then 1 symbol", 400
    # Serching by director
    elif operation == 'director':
        if search_empty_fields(text):
            search = "%{}%".format(text)
            if ascending == 'ascending':
                search_last_name = Film.query.join(Film.fk_director_id). \
                    filter(Director.last_name.like(search)) \
                    .order_by(sort_variable).paginate(page=pagin).items
            else:
                search_last_name = Film.query.join(Film.fk_director_id). \
                    filter(Director.last_name.like(search)). \
                    order_by(db.desc(sort_variable)).paginate(page=pagin).items
            if search_last_name:
                return search_last_name
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    # Serching by genre
    elif operation == 'genre':
        if search_empty_fields(text):
            if ascending == 'ascending':
                search_genre = Film.query.join(Film.fk_genre_id) \
                    .filter(Genre.title.like(text)).order_by(sort_variable) \
                    .paginate(page=pagin).items
            else:
                search_genre = Film.query.join(Film.fk_genre_id) \
                    .filter(Genre.title.like(text)).order_by(db.desc(sort_variable)) \
                    .paginate(page=pagin).items
            if search_genre:
                return search_genre
            return "Films not found", 404
        return "Len should be more then 1 symbol", 400
    # Serching by relisedate
    elif operation == 'relisedate':
        if ascending == 'ascending':
            search_relisedate = Film.query.filter(
                Film.release > lower_year + '-01-01',
                Film.release < upper_year + '-12-31') \
                .order_by(sort_variable) \
                .paginate(page=pagin).items
        else:
            search_relisedate = Film.query.filter(
                Film.release > lower_year + '-01-01',
                Film.release < upper_year + '-12-31').order_by(db.desc(sort_variable)) \
                .paginate(page=pagin).items
        if search_relisedate:
            return search_relisedate
        return "Films not found", 404


# .order_by(Film.rating)

@api.route('/films-api/Search-reting-Sort')
class SortRetingSearchFilms(Resource):
    """Searching films by genre, director, relisedate, sort by rating"""

    @api.marshal_with(model_film, code=200)
    @api.doc("Searching and sort films.")
    def get(self):
        """Choose operation and searching films"""
        upper_year = str(datetime.datetime.now().year)
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, default='none')  # arg for director and genre
        parser.add_argument('operation', type=str, default='none')  # search by genre, director, relisedate
        parser.add_argument('pagination', type=int, default=1)
        parser.add_argument('lower_year', type=str, default='1900')
        parser.add_argument('upper_year', type=str, default=upper_year)
        parser.add_argument('ascending', type=str, default='descending')  # kind of sort
        parser.add_argument('sorting_var', type=str, default='')  # rating or release
        args = parser.parse_args()
        res = search_operation_sort_rating(args['text'], args['operation'], args['ascending'],
                                           args['pagination'], args['lower_year'],
                                           args['upper_year'], args['sorting_var'])
        if current_user.is_active:
            film_log.save_logs(f"User id: {current_user.id};"
                               f" operation: {args['operation']}; "
                               f" class SortRetingSearchFilms")
        return db.session.query(Film).filter(Film.id == args['id']).first()


def add_up_del_operation(film_id, title, release, poster,
                         rating, description, dir_id, genre):
    if not (title or release or poster or rating or description
            or dir_id or genre):
        abort(403, "At least one field should be filled")
    if not film_id:
        abort(403, "Film not found")
    film_found = db.session.query(Film).filter(Film.id == film_id).first()
    if not (current_user.id == film_found.fk_user_id or current_user.id == 1):
        abort(403, "Not enough rights")
    field = 'field'
    try:
        if title:
            field = 'title'
            film_found.title = title
        if release:
            field = 'release'
            film_found.release = release
        if poster:
            field = 'poster'
            film_found.poster = poster
        if rating:
            field = 'rating. Min 1; Max 10'
            if rating > 10 or rating < 1:
                abort(403, "Incorrect rating. Min 1; Max 10")
            film_found.rating = rating
        if description:
            field = 'description'
            film_found.description = description
        if dir_id:
            field = 'chosen director'
            dir_id = dir_id.strip().split()
            new_dirs = []
            for direct in dir_id:
                find_dir = db.session.query(Director). \
                    filter(Director.id == direct).first()
                if find_dir:
                    new_dirs.append(find_dir)
            film_found.fk_director_id = new_dirs
            # print(film_found.fk_director_id)
        if genre:
            field = 'chosen genre'
            genre = genre.strip().split()
            new_genre = []
            for gen in genre:
                find_gen = db.session.query(Genre).filter(Genre.id == gen).first()
                if find_gen:
                    new_genre.append(find_gen)
            film_found.fk_genre_id = new_genre
            # print(film_found.fk_genre_id)
    except:
        abort(403, f'Incorrectly {field}')
    db.session.commit()


@api.route('/films-api/up-film')
class UpFilm(Resource):
    """Update films"""

    @login_required
    @api.marshal_with(model_film, code=200)
    @api.doc("Chenge fields in films")
    def put(self):
        """Updating any field of chosen film"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, default=None)
        parser.add_argument('title', type=str, default=None)
        parser.add_argument('release', type=str, default=None)
        parser.add_argument('poster', type=str, default=None)
        parser.add_argument('rating', type=int, default=None)
        parser.add_argument('description', type=str, default=None)
        parser.add_argument('dir_id', type=str, default=None)
        parser.add_argument('genre', type=str, default=None)
        args = parser.parse_args()
        add_up_del_operation(args['id'], args['title'], args['release'],
                             args['poster'], args['rating'],
                             args['description'], args['dir_id'],
                             args['genre'])
        film_log.save_logs(f"User id: {current_user.id};"
                           f" Update film id: {args['id']}")
        return db.session.query(Film).filter(Film.id == args['id']).first()


@api.route('/films-api/film-delete')
class DelFilm(Resource):
    """Delete film"""

    @login_required
    @api.marshal_with(model_del_director, code=200)
    @api.doc("Change fields in films")
    def delete(self):
        """Film delete method"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, default=None)
        args = parser.parse_args()
        film_to_del = db.session.query(Film).filter(Film.id == args['id']).first()
        if not film_to_del:
            abort(403, 'Film not found.')
        if not (current_user.id == film_to_del.fk_user_id or current_user.id == 1):
            abort(403, "Not enough rights")
        id_deleted_film = film_to_del.id
        db.session.delete(film_to_del)
        db.session.commit()
        film_log.save_logs(f"User id: {current_user.id};"
                           f" Delete film id: {args['id']}")
        return {'id': id_deleted_film, 'deleted': True}


def director_delete(direct_id):
    """Deleting director"""
    director_to_del = db.session.query(Director).filter(Director.id == direct_id).first()
    if not director_to_del:
        abort(403, 'Director not found.')
    if not current_user.id == 1:
        abort(403, "Not enough rights")
    change_film_dir = db.session.query(Filmdirector).filter(Filmdirector.director_id == direct_id).all()
    films_dir_unknown = []
    if len(change_film_dir):
        for dir_change in change_film_dir:
            dir_change.director_id = 1  # unknown director
            films_dir_unknown.append(dir_change.film_id)
            db.session.commit()
    id_deleted_director = director_to_del.id
    db.session.delete(director_to_del)
    db.session.commit()
    film_log.save_logs(f"User id: {current_user.id};"
                       f" Delete director id: {id_deleted_director}"
                       f" Films id: {films_dir_unknown} where director 'unknown'")
    return id_deleted_director


@api.route('/films-api/director-delete')
class DelDirector(Resource):
    """Delete director"""

    @login_required
    @api.marshal_with(model_del_director, code=200)
    @api.doc("Delete director.")
    def delete(self):
        """Director delete method"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, default=None)
        args = parser.parse_args()
        if args['id']:
            del_id = director_delete(args['id'])
            return {'id': del_id, 'deleted': True}


def find_dir(first_n, last_n):
    """Abort if director already exist"""
    director_find = db.session.query(Director).filter(Director.first_name == first_n.title(),
                                                      Director.last_name == last_n.title()).first()
    return director_find


@api.route('/films-api/director-add')
class AddDirector(Resource):
    """Add new director"""

    @login_required
    @api.marshal_with(model_add, code=200)
    @api.doc("Create new director.")
    def post(self):
        """Director add method"""
        # if not current_user.id == 1:    # Admin rights only
        #     abort(403, "Not enough rights")
        parser = reqparse.RequestParser()
        parser.add_argument('first', type=str, default=None)
        parser.add_argument('last', type=str, default=None)
        args = parser.parse_args()
        if not (args['first'] or args['last']):
            abort(403, "All fields must be filled")
        check_find_dir = find_dir(args['first'], args['last'])
        if check_find_dir:
            abort(403, "Director already exists")
        new_dir = Director(first_name=args['first'].title(), last_name=args['last'].title())
        db.session.add(new_dir)
        db.session.commit()
        added_dir = find_dir(args['first'], args['last'])
        added_id = added_dir.id
        film_log.save_logs(f"User id: {current_user.id};"
                           f" New director id: {added_id} added")
        return {'id': added_id, 'added': True}


def find_gen(gen_t):
    """Abort if title already exist"""
    genre_find = db.session.query(Genre).filter(Genre.title == gen_t.title()).first()
    return genre_find


@api.route('/films-api/genre-add')
class AddGenre(Resource):
    """Add new genre"""

    @login_required
    @api.marshal_with(model_add, code=200)
    @api.doc("Create new genre.")
    def post(self):
        """Genre add method"""
        # if not current_user.id == 1:   # Admin rights only
        #     abort(403, "Not enough rights")
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, default=None)
        args = parser.parse_args()
        if not args['title']:
            abort(403, "Field must be filled")
        check_find_gen = find_gen(args['title'])
        if check_find_gen:
            abort(403, "Genre already exists")
        new_gen = Genre(title=args['title'].title())
        db.session.add(new_gen)
        db.session.commit()
        added_gen = find_gen(args['title'])
        added_id = added_gen.id
        film_log.save_logs(f"User id: {current_user.id};"
                           f" New genre id: {added_id} added")
        return {'id': added_id, 'added': True}


def find_film_check(film_tit):
    """Abort if title already exist"""
    film_ti_find = db.session.query(Film).filter(Film.title == film_tit.title()).first()
    return film_ti_find


def find_dir_check(direc_id):
    """Abort if director not found or create list with directors"""
    direc_id = direc_id.strip().split()
    new_dirs = []
    for dir in direc_id:
        dir_found = db.session.query(Director).filter(Director.id == dir).first()
        if not dir_found:
            abort(403, "Director not found. Create director first")
        new_dirs.append(dir_found)
    return new_dirs


def find_gen_check(genr_id):
    """Abort if genre not found or create list with genres"""
    genr_id = genr_id.strip().split()
    new_genrs = []
    for id_g in genr_id:
        gen_found = db.session.query(Genre).filter(Genre.id == id_g).first()
        if not gen_found:
            abort(403, "Genre not found. Create genre first")
        new_genrs.append(gen_found)
    return new_genrs


@api.route('/films-api/film-add')
class AddFilm(Resource):
    """Add new film"""

    @login_required
    @api.marshal_with(model_add, code=200)
    @api.doc("Create new film.")
    def post(self):
        """Film add method"""
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, default=None)
        parser.add_argument('release', type=str, default=None)
        parser.add_argument('poster', type=str, default=None)
        parser.add_argument('rating', type=int, default=None)
        parser.add_argument('description', type=str, default=None)
        parser.add_argument('dir_id', type=str, default=None)
        parser.add_argument('genre_id', type=str, default=None)
        args = parser.parse_args()
        if not (args['title'] and args['release'] and args['poster'] and
                args['rating'] and
                args['dir_id'] and args['genre_id']):
            abort(403, "All field should be filled")
        check_film = find_film_check(args['title'])
        if check_film:
            abort(403, "Film title already exists")
        if args['rating'] > 10 or args['rating'] < 1:
            abort(403, "Incorrect rating. Min 1; Max 10")
        new_directors = find_dir_check(args['dir_id'])
        new_genres = find_gen_check(args['genre_id'])
        try:
            new_film = Film(title=args['title'].title(), release=args['release'],
                            poster=args['poster'], rating=args['rating'],
                            description=args['description'], fk_user_id=current_user.id)
            db.session.add(new_film)
            db.session.commit()
        except:
            abort(403, "Incorrect entered data")
        find_new_film = find_film_check(args['title'])
        find_new_film.fk_director_id = new_directors
        find_new_film.fk_genre_id = new_genres
        db.session.commit()
        added_id = find_new_film.id
        film_log.save_logs(f"User id: {current_user.id};"
                           f" New film id: {added_id} added")
        return {'id': added_id, 'added': True}
