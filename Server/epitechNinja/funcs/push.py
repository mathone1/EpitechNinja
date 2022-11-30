from typing import List
from flask import current_app
from pywebpush import webpush, WebPushException
import json


def sendPushNotifications(title: str, body: str, subscription: str):

  private_key = current_app.config.get('VAPID_PRIVATE_KEY')
  claim = current_app.config.get('VAPID_CLAIM_EMAIL')

  try:
    response = webpush(
      subscription_info=json.loads(subscription),
      data=json.dumps({'title': title, 'body': body}),
      vapid_private_key=private_key,
      vapid_claims={
        'sub':'mailto:{0}'.format(claim)
      }
    )
    return response.ok
  except WebPushException as e:
    if e.response and e.response.json():
      extra = e.response.json()
      print('Remote service replied with {0}:{1}, {2}'.format(extra.code, extra.errno, extra.message))

    return False


def triggerPushNotifications(title: str, body: str, subscriptions: List[str]):

  return [sendPushNotifications(title, body, subscription) for subscription in subscriptions]
