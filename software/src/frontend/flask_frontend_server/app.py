from flask import Flask, render_template
from flask_sock import Sock
from software.src.backend.tracker.face_detector import run_face_tracking, get_commands_simple
import asyncio
from websockets.asyncio.server import serve
import time
import threading
import json

class Data:
    def __init__(self):
        self.motorcmmds = "Stop"
        self.size = None

    def get_motor(self):
        return self.motorcmmds

    def set_motor(self, cmmds):
        self.motorcmmds = cmmds


session = Data()
def main_app_server():
    app = Flask(__name__)
    sock = Sock(app)

    

    # This route serves your HTML file when anyone visits your website
    @app.route('/')
    def index():
        return render_template('index.html')

    @sock.route('/stream')
    def echo(sock):
        while True:
            data = sock.receive()
            
            
        
            motor_movements = get_commands_simple(data)
            image, _, _ = run_face_tracking(data)

            session.set_motor(cmmds=motor_movements)
            
            print(motor_movements)

            
            
            with open("im.jpg", "wb") as f:
                f.write(image)
        
           
    
    if __name__ == '__main__':
        # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
        app.run(host="0.0.0.0", port=5555, debug=True, ssl_context="adhoc", use_reloader=False)



#second server to serve the arduino motor commands
def arduino_server():
    app = Flask(__name__)
    sock = Sock(app)

    @sock.route('/stream')
    def stream(ws):
        while True:

            time.sleep(1)

            ws.send(json.dumps(session.get_motor()))

            


    app.run(host="0.0.0.0", port=5556, use_reloader=False)  # no ssl_context


        
thread1 = threading.Thread(target=main_app_server)
thread2 = threading.Thread(target=arduino_server)

thread1.start()
thread2.start()



