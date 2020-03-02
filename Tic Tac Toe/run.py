# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

from xo import socketio,app

if __name__ == '__main__':
  socketio.run( app, host='0.0.0.0' ,debug = True )

   