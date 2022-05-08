import os

from flask_app import app
from slack_bot import bot, socket_handler

import slack_bot.event_handlers
import flask_app.routes


# Open a WebSocket connection
socket_handler.connect()

# Run Flask app
if os.environ.get('MODE') != 'production':
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run()
