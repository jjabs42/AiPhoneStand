# arduino_server.py — plain HTTP, for the R4
from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@sock.route('/stream')
def stream(ws):
    while True:
        data = ws.receive()
        if not data:
            break
        print(data)

        ws.send("Hello")

        


app.run(host="0.0.0.0", port=5556)  # no ssl_context