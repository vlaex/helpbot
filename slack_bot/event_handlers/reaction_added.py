import re
from slack_bot import bot
from slack_bot.utils.slack_messages import delete_message, get_delete_reason
from slack_bot.config import admins, channels, reactions, PROFILE_LINK_REGEX
from slack_bot.core.sheets import sheet
from slack_bot.utils.ts_to_date import ts_to_date
from slack_bot.core.users import SlackUser


@bot.event('reaction_added')
def handle_reaction_added_event(event, context):
  reaction = event['reaction']
  user = context['user_data']
  user_id = user['id']
  channel = event['item']['channel']
  message_ts = event['item']['ts']
  event_ts = event['event_ts']

  message = context['message']

  if 'pinned_to' in message or 'subtype' in message:
    return

  if reaction == 'test_tube' and user_id in admins:
    delete_message(channel_id=channel, ts=message_ts)
    return

  if channel == channels['HELP'] and re.search(reactions['REGEX'], reaction):
    delete_message(channel_id=channel, ts=message_ts)

    sheet.worksheet('#help').insert_row([
      ts_to_date(message_ts),
      context['message_user']['profile']['display_name'] or context['message_user']['name'],
      message['text'],
      context['user_nick'],
      ts_to_date(event_ts)
    ], 2)
  elif channel == channels['ANTISPAMERS'] and 'bot_profile' in message:
    delete_message(channel_id=channel, ts=message_ts)

    blocks = message['blocks']
    user_id = re.search(r"(?<=<@)[A-Z0-9]*", blocks[2]['elements'][0]['text']).group()

    sheet.worksheet('Принятые репорты').insert_row([
      re.search(r"https.+(?=>)", blocks[0]['text']['text']).group(),
      SlackUser(user_id).get_nick(),
      context['user_nick'],
      ts_to_date(event_ts)
    ], 2)
  elif channel == channels['TO_DELETE']:
    if event['user'] not in admins or reaction not in reactions['TO_DELETE']:
      return

    delete_message(channel_id=channel, ts=message_ts)

    message_text = message['text']

    profile_link = re.search(PROFILE_LINK_REGEX, message_text)
    delete_reason = get_delete_reason(message_text)

    sheet.worksheet('#to-delete').insert_row([
      delete_reason,
      profile_link.group() if profile_link else '?',
      context['message_user_nick'],
      ts_to_date(message_ts),
      ts_to_date(event_ts),
      message_text
    ], 2)
