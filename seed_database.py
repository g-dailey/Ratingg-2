"""Script to seed database."""

import os
import json
from pickletools import read_stringnl_noescape_pair
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
  movie_data = json.loads(f.read())

movies_in_db = []

for movie in movie_data:
  date = movie['release_date']
  format2 = "%Y-%m-%d"
  release_date = datetime.strptime(date, format2).date()
  title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"])
  db_movie = crud.create_movie(title, overview, release_date, poster_path)
  movies_in_db.append(db_movie)


model.db.session.add_all(movies_in_db)
model.db.session.commit()

list_of_users = []
for n in range(10):
  email = f'user{n}@test.com'
  password = 'test'
  db_user = crud.create_user(email, password)
  model.db.session.add(db_user)

  for _ in range(10):
    random_movie = choice(movies_in_db)
    score = randint(1,5)

    ratings = crud.create_rating(db_user, random_movie, score)
    model.db.session.add(ratings)

model.db.session.commit()
