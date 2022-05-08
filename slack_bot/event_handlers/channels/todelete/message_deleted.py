from slack_bot.core.redis_db import redis_client
from slack_bot import bot
from slack_bot.config import channels
from slack_bot.utils.slack_messages import get_delete_reason


@bot.event(
  event='message',
  matchers=[
    lambda event: event.get('subtype') == 'message_deleted' and event['channel'] == channels['TO_DELETE'],
    lambda event: get_delete_reason(event['previous_message']['text']) != ''
  ]
)
def handle_message_deleted_event(event):
  previous_message = event['previous_message']

  redis_client.delete(f"todelete:{previous_message['ts']}:{previous_message['user']}")
