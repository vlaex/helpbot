from flask import Flask
from flask_cors import CORS
from flask_sock import Sock

app = Flask('helpbot')

CORS(app)

sock = Sock(app)

@sock.route('/todelete/live')
def echo(ws):
  while True:
    data = ws.receive()
    ws.send(data)
