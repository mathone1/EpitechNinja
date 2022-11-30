from flask import Blueprint, request


push = Blueprint('push', __name__)


@push.route('/', methods=['POST'])
def addPush():
  from epitechNinja.db import db

  subscription = request.get_json().get('subscription')

  dbSubscription = db.push.find_one({'subscription': subscription})

  if dbSubscription is None:
    id = db.push.insert_one({'subscription': subscription}).inserted_id
  else:
    id = dbSubscription  #.get('_id')

  return {
      'status': 1,
      'id': str(id),
      'subscription': subscription
    }, 200
