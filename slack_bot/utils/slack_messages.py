import os
import re
from typing import Optional
from slack_bolt.error import BoltError
from slack_bot import bot
from slack_bot.config import DELETE_REASON_REGEX


def get_delete_reason(text: str):
  match = re.search(DELETE_REASON_REGEX, text, re.IGNORECASE)

  if match is None:
    return ''

  return re.sub(r"(^,|-)\s*|\.$", '', match.group()).strip().capitalize()


def get_message(channel: str, ts: str):
  messages = bot.client.conversations_history(
    limit=1,
    channel=channel,
    inclusive=True,
    latest=ts
  )

  for message in messages['messages']:
    if message['ts'] == ts:
      return message


def delete_message(channel_id: str, ts: str, clear_threads: Optional[bool]=True):
  try:
    if clear_threads:
      replies = bot.client.conversations_replies(channel=channel_id, ts=ts)
      for reply in replies['messages']:
        if 'parent_user_id' not in reply:
          continue
      
        bot.client.chat_delete(
          token=os.environ['SLACK_ADMIN_TOKEN'],
          ts=reply['ts'],
          channel=channel_id
        )

    bot.client.chat_delete(
      token=os.environ['SLACK_ADMIN_TOKEN'],
      ts=ts,
      channel=channel_id
    )
  except Exception:
    pass
