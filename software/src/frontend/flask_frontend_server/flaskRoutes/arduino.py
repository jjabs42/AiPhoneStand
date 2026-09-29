from ..utils import connect
from flask_sock import Sock
import time

#route for arduino ws basically connects the socket

def registerArduino(sock):
    @sock.route('/stream')
    def stream(ws: Sock):

        #connects ws and shares the object so every file can access it
        connect(ws)

        while True:
            message = ws.receive()
            print(message)
            time.sleep(0.01)
            message: str
            x = message.strip().split(",")
            print(x)
            x = int(x)
            y = int(y)

            print(x,y)


        

