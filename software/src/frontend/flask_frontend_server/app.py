from flask import Flask, render_template
from flask_sock import Sock
import threading
import numpy as np
from .flaskRoutes import registerSocket, registerArduino




def main_app_server():
    app = Flask(__name__)
    sock = Sock(app)

    

    # This route serves your HTML file when anyone visits your website
    @app.route('/')
    def index():
        return render_template('index.html')

    registerSocket(sock)

    if __name__ == '__main__':
        # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
        app.run(host="0.0.0.0", port=5555, debug=True, ssl_context="adhoc", use_reloader=False)



#second server to serve the arduino face commands
def arduino_server():
    app = Flask(__name__)
    sock = Sock(app)

    registerArduino(sock)

    
    app.run(host="0.0.0.0", port=5556, use_reloader=False)  # no ssl_context


        
thread1 = threading.Thread(target=main_app_server)
thread2 = threading.Thread(target=arduino_server)

thread1.start()
thread2.start()



