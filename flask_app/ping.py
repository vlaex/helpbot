from . import app

@app.route('/ping')
def pong():
  return {'message': 'Pong!'}
