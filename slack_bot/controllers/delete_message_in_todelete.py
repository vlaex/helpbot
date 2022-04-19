import re
from slack_bot.utils.slack_messages import delete_message
from slack_bot.utils.sheets import sheet
from slack_bot.utils.get_user import get_user_nick
from slack_bot.utils.ts_to_date import ts_to_date

def delete_message_in_todelete(channel: str, event_ts: str, message):
  delete_message(channel_id=channel, ts=message['ts'], clear_threads=True)

  profile_link = re.search(
    r"(?<=<)[A-Za-z:\/]+znanija\.com\/((app\/profile\/)|(profil\/\w+-)|(users\/user_content\/))\d+",
    message['text']
  )
  delete_reason = re.search(r"(?<=(?<=>)\s|\|)\w+", message['text'])

  sheet.worksheet('#to-delete').insert_row([
    delete_reason.group() if delete_reason else '?',
    profile_link.group() if profile_link else 'https://znanija.com/profil/Incognito-0',
    get_user_nick(message['user']),
    ts_to_date(message['ts']),
    ts_to_date(event_ts),
    message['text']
  ], 2)
