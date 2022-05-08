import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


bot = App(
  signing_secret=os.environ['SLACK_SIGNING_SECRET'],
  token=os.environ['SLACK_BOT_TOKEN']
)

socket_handler = SocketModeHandler(bot, os.environ['SLACK_APP_TOKEN'])
