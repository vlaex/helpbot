import os
from datetime import datetime
from flask import abort
from slack_bot import bot
from slack_bot.controllers.delete_message_in_todelete import delete_message_in_todelete
from . import app

@app.post('/delete_user/<user_id>')
def delete_user(user_id: int):
  try:
    user_id = int(user_id)

    if user_id <= 3:
      raise ValueError

    # Find messages by user ID
    user_token = os.environ['SLACK_USER_TOKEN']
    search_results = bot.client.search_messages(
      query=f"{user_id} in:#to-delete",
      sort='score',
      sort_dir='desc',
      token=user_token
    )

    messages = search_results['messages']

    if messages['total'] < 1:
      return 'Message not found'

    for message in messages['matches']:
      delete_message_in_todelete(
        channel=message['channel']['id'],
        event_ts=str(datetime.now().timestamp()),
        message=message
      )

    return {
      'deleted': True,
      'user_id': user_id,
      'matches': len(messages['matches'])
    }
  except ValueError:
    print('An error occured while trying to parse user ID')
    abort(400)
