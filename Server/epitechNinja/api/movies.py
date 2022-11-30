from flask import Blueprint


movies = Blueprint('movies', __name__)


@movies.route('/', methods=['GET'])
def getMovies():
  from epitechNinja.db import db
  from epitechNinja.models.Movie import Movie

  try:

    others = []

    for movie in db.movies.find({}, {'_id': 0}):
      others.append(Movie.fromDict(movie).toFrontEnd())

    total = db.movies.count_documents({})

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return {
      'status': 1,
      'movies': others,
      'total': total
    }, 200
