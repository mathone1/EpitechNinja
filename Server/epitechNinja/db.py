from flask import current_app
from pymongo import MongoClient

URI = current_app.config.get('DB_URI')
# ! if URI is None or database is None:
# ! kill + send Alert !!!
db = MongoClient(URI)['EpitechNinja']
