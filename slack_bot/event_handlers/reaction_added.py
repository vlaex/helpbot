import re
from slack_bot import bot
from slack_bot.utils.slack_messages import get_message, delete_message
from slack_bot.utils.sheets import sheet
from slack_bot.utils.get_user import get_user_nick
from slack_bot.utils.ts_to_date import ts_to_date
from slack_bot.config import admins, channels, reactions
from slack_bot.controllers.delete_message_in_todelete import delete_message_in_todelete

@bot.event('reaction_added')
def handle_reaction_added_event(event):
  channel = event['item']['channel']
  message_ts = event['item']['ts']

  if event['reaction'] == 'test_tube' and event['user'] in admins:
    delete_message(channel_id=channel, ts=message_ts)
    return

  message = get_message(channel=channel, ts=message_ts)
  if message is None:
    print(f"Seems like this message does not exist in channel {channel}")
    return

  if 'pinned_to' in message or 'subtype' in message:
    return

  # Delete bot messages in #antispamers
  if channel == channels['ANTISPAMERS'] and 'bot_profile' in message:
    delete_message(channel_id=channel, ts=message['ts'])

    blocks = message['blocks']

    deleted_by_user = get_user_nick(event['user'])
    
    sender_id = re.search(r"(?<=<@)[A-Z0-9]*", blocks[2]['elements'][0]['text']).group()
    sender_nick = get_user_nick(sender_id)

    sheet.worksheet('Принятые репорты').insert_row([
      re.search(r"https.+(?=>)", blocks[0]['text']['text']).group(),
      sender_nick,
      deleted_by_user,
      ts_to_date(event['event_ts'])
    ], 2)

    return

  # Delete message in #help
  if channel == channels['HELP'] and re.search(reactions['REGEX'], event['reaction']):
    delete_message(channel_id=channel, ts=message['ts'])

    message_sent_by = get_user_nick(message['user'])
    message_deleted_by = get_user_nick(event['user'])

    sheet.worksheet('#help').insert_row([
      ts_to_date(message['ts']),
      message_sent_by,
      message['text'],
      message_deleted_by,
      ts_to_date(event['event_ts'])
    ], 2)

    return

  # Delete message in #to-delete
  if channel == channels['TO_DELETE']:
    if event['user'] not in admins or event['reaction'] not in reactions['TO_DELETE']:
      return

    delete_message_in_todelete(
      channel=channel,
      event_ts=event['event_ts'], 
      message=message
    )
