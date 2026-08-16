from flask import Flask, render_template
from flask_sock import Sock
from software.src.backend.tracker.face_detector import run_face_tracking, get_commands
import asyncio
from websockets.asyncio.server import serve
import time


class Data:
    def __init__(self):
        self.data = None

    def get(self):
        return self.data

    def set(self, data):
        self.data = data


app = Flask(__name__)
sock = Sock(app)

data = Data()

# This route serves your HTML file when anyone visits your website
@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/stream')
def echo(sock):
    while True:
        a = time.time()
        data = sock.receive()
        
        print(get_commands(data))

        image, face_pts, center = run_face_tracking(data)

        

        with open("im.jpg", "wb") as f:
            f.write(image)
        b = time.time()
        print(b-a)


        


        

if __name__ == '__main__':
    # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
    app.run(host="0.0.0.0", port=5555, debug=True, ssl_context="adhoc")