import os
from flask import jsonify
from flask_app import app
from flask_cors import cross_origin
from slack_bot import bot
from slack_bot.config import channels


@app.post('/delete_user/<user_id>')
@cross_origin(
  origins=['https://znanija.com', 'https://brainly.com']
)
def delete_message_by_user(user_id: int):
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

    bot.client.reactions_add(
      token=user_token,
      channel=channels['TO_DELETE'],
      name='canc_noj',
      timestamp=messages['matches'][0]['ts']
    )

    return jsonify(user_id=user_id, matches=len(messages['matches']))
  except ValueError:
    return 'An error occured while trying to parse user ID', 400
