from flask import Blueprint, request


progress = Blueprint('progress', __name__)


@progress.route('/<id>', methods=['GET'])
def getProgress(id=None):
  from epitechNinja.db import db

  if id is None:
    return {'status': 0, 'error': 'Id is required.'}, 400

  try:
    id = int(id)
  except:
    return {'status': 0, 'error': 'Id is invalid.'}, 400

  try:

    progress = db.progress.find_one({'userId': id})

    if progress is None:
      return {
        'status': 1,
        'movies': [],
        'shows': []
      }, 200

    movies = progress.get('movies', [])
    shows = progress.get('shows', [])

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return {
      'status': 1,
      'movies': movies,
      'shows': shows
    }, 200


@progress.route('/movie/<movieId>/<userId>', methods=['GET'])
def getMovieProgress(movieId=None, userId=None):
  from epitechNinja.db import db

  if userId is None:
    return {'status': 0, 'error': 'Id is required.'}, 400

  try:
    userId = int(userId)
  except:
    return {'status': 0, 'error': 'Id is invalid.'}, 400

  try:

    if movieId is None:
      return {'status': 0, 'error': 'The movie ID is required.'}, 400

    progress = db.progress.find_one({'userId': userId, 'movies.tmdbId': movieId})

    if progress is None:
      return {
        'status': 1,
        'progress': 0
      }, 200

    movieProgress = next(x.get('progress') for x in progress.get('movies') if x.get('tmdbId') == movieId)

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return {
      'status': 1,
      'progress': movieProgress
    }, 201


@progress.route('/movie/<movieId>/<userId>', methods=['POST'])
def saveMovieProgress(movieId=None, userId=None):
  from epitechNinja.funcs.push import triggerPushNotifications
  from epitechNinja.db import db
  from epitechNinja.models.Movie import Movie

  if userId is None:
    return {'status': 0, 'error': 'Id is required.'}, 400

  try:
    userId = int(userId)
    movieIdInt = int(movieId)
  except:
    return {'status': 0, 'error': 'Id is invalid.'}, 400

  try:

    if movieId is None:
      return {'status': 0, 'error': 'The movie ID is required.'}, 400

    progress = request.get_json().get('progress')

    if progress is None or not isinstance(progress, int):
      return {'status': 0, 'error': 'The progress is required and must be an integer.'}, 400

    if db.progress.count_documents({'userId': userId, 'movies.tmdbId': movieId}) > 0:
      db.progress.update_one({'userId': userId, 'movies.tmdbId': movieId}, {'$set': {'movies.$.progress': progress}})

    else:
      db.progress.update_one({'userId': userId, 'movies.tmdbId': {'$ne': movieId}}, {'$addToSet': {'movies': {'tmdbId': movieId, 'progress': progress}}}, upsert=True)

    if userId != 100:  # 0
      subscriptions = [x.get('subscription') for x in db.push.find({})]
      movieDict = db.movies.find_one({'tmdbId': movieIdInt})

      if movieDict is None:
        return {'status': 0, 'error': 'Invalid movieId.'}, 400

      movie = Movie.fromDict(movieDict)
      title = "{0} {1} a movie:".format('Mathieu' if userId == 1 else 'Thomas', 'watched' if progress == -1 else ('unwatched' if progress == 0 else 'stopped watching'))
      body = "{0}".format(movie.title.en)

      triggerPushNotifications(
        title=title,
        body=body,
        subscriptions=subscriptions
      )

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return {
      'status': 1,
      'description': 'Progress successfully saved.'
    }, 201
