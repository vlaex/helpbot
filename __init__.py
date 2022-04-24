import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import request

from flask_app import app
from slack_bot import bot

# Init event handlers here
import slack_bot.event_handlers.message_sent
import slack_bot.event_handlers.reaction_added
import slack_bot.event_handlers.errors

# Init Flask listeners here
import flask_app.delete_messages_by_user
import flask_app.ping

# Open WebSocket connection

socket_handler = SocketModeHandler(bot, os.environ['SLACK_APP_TOKEN'])
socket_handler.connect()

if os.environ.get('MODE') != 'production':
  app.run()
