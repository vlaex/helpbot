import os
from datetime import datetime
from flask import make_response, render_template
from flask_app import app


@app.get('/')
def homepage():
  server_time = datetime.now().strftime("%d %a %Y, %H:%M:%S")
  mode = os.environ['MODE']

  res = make_response(
    render_template('homepage.html', server_time=server_time, mode=mode)
  )

  res.headers['x-bot-mode'] = os.environ['MODE']
  res.headers['cache-control'] = 'max-age=300'
  
  return res
