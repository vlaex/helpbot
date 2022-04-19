import os
from slack_bolt import App

bot = App(
  signing_secret=os.environ['SLACK_SIGNING_SECRET'],
  token=os.environ['SLACK_BOT_TOKEN']
)
