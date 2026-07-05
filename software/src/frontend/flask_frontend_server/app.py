from flask import Flask, render_template
from flask_sock import Sock



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
        with open("frame.jpg", "wb") as f:
            f.write(data)


        

if __name__ == '__main__':
    # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
    app.run(host="0.0.0.0", port=5555, debug=True)