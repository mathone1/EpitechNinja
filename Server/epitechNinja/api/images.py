from flask import Blueprint, send_file


images = Blueprint('images', __name__)


@images.route('/movie/<id>/<image>/<lang>', methods=['GET'])
def getMovieImage(id=None, image=None, lang='en'):
  from flask import current_app

  if id is None:
    return {
          'status': 0,
          'error': 'An id is required',
      }, 400

  if image.lower() != 'poster' and image.lower() != 'backdrop':
    return {
          'status': 0,
          'error': "Image type must be 'poster' or 'backdrop'.",
      }, 400

  if lang.lower() != 'en' and lang.lower() != 'fr':
    return {
          'status': 0,
          'error': "Image type must be 'en' or 'fr'.",
      }, 400

  try:

    dataPath = current_app.config.get('DATA_PATH')
    imagePath = "{0}/movies/{1}/{2}_{3}.jpg".format(dataPath, id, image.lower(), lang.lower())

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return send_file(imagePath, mimetype='image/jpg'), 200


@images.route('/actor/<id>', methods=['GET'])
def getActorImage(id=None):
  from flask import current_app

  if id is None:
    return {
          'status': 0,
          'error': 'An id is required',
      }, 400

  try:

    dataPath = current_app.config.get('DATA_PATH')
    imagePath = "{0}/actors/{1}.jpg".format(dataPath, id)

  except Exception as e:
    return {
          'status': 0,
          'error': 'Invalid data.',
          'exception': str(e)
      }, 400

  return send_file(imagePath, mimetype='image/jpg'), 200
