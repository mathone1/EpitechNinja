from flask import Flask
from flask_cors import CORS

from epitechNinja.api.movies import movies
from epitechNinja.api.images import images
from epitechNinja.api.progress import progress
from epitechNinja.api.push import push


def create_app(conf):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(conf)

    app.register_blueprint(movies, url_prefix="/movies")
    app.register_blueprint(images, url_prefix='/images')
    app.register_blueprint(progress, url_prefix='/progress')
    app.register_blueprint(push, url_prefix="/push")

    return app
