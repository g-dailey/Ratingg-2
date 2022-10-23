from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_movie(title, overview, release_date, poster_path):
  movie = Movie(title=title,
                overview=overview,
                release_date=release_date,
                poster_path=poster_path,
                )
  return movie


def get_movies():
  return Movie.query.all()

def get_movie_by_id(movie_id):
  return Movie.query.get(movie_id)

def get_users():
  return User.query.all()

def get_user_by_email(email):
  return User.query.filter(User.email == email).first()

def create_rating(user, movie, score):
  rating = Rating(user=user, movie=movie, score=score)

  return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)