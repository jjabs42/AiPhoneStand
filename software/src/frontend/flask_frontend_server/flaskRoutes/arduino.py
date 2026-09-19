from ..utils import connect
from flask_sock import Sock
#route for arduino ws

def registerArduino(sock):
    @sock.route('/stream')
    def stream(ws: Sock):

        #connects ws and shares the object so every file can access it
        connect(ws)

        while True:
            message = ws.receive()
            print(message)

        

