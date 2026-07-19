from flask import Flask, render_template
from flask_sock import Sock
from software.src.backend.tracker.face_detector import run_face_tracking, get_commands
import time



app = Flask(__name__)
sock = Sock(app)

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

        image, face_pts, center  = run_face_tracking(data)

        

        with open("im.jpg", "wb") as f:
            f.write(image)
        b = time.time()
        print(b-a)


        


        

if __name__ == '__main__':
    # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
    app.run(host="0.0.0.0", port=5555, debug=True, ssl_context="adhoc")