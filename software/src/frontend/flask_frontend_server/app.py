from flask import Flask, render_template
from flask_sock import Sock
from software.src.backend.tracker import run_face_tracking, motor_angle
from websockets.asyncio.server import serve
from utils import direction, toImage
import time
import threading
import json
import base64
import cv2
import numpy as np




#constants
pxByDegrees = 0
calibrationDegrees = 30

class Data:
    def __init__(self):
        self.data = ""
        self.calibrateR = False
        self.clickedCal = False
        self.dataReady = False
        self.conversion = 0
        self.motorData = []
        
        










session = Data()
def main_app_server():
    app = Flask(__name__)
    sock = Sock(app)

    

    # This route serves your HTML file when anyone visits your website
    @app.route('/')
    def index():
        return render_template('index.html')


    #path for the websocket for sending image data
    @sock.route('/stream')
    def echo(sock):
        while True:

            #receives payload
            data = sock.receive()
            
            #converts raw data into json
            try:
                jsonData = json.loads(data)
            except Exception as e:
                print(e)

            print(jsonData.get("CalibrationInitiated"))
            if jsonData.get("CalibrationInitiated") == True:
                session.clickedCal = True


            
            #saying that if the thing we want to do is calibrate, then we calibrate
            elif jsonData.get("action") == "CalibrationActive":

                #receives first photo for calibration
                frame1Raw = sock.receive()
                try:
                    frame1 = json.loads(frame1Raw)
                except Exception as e:
                    print(e)

                #saves facing mode
                facingMode = frame1.get("facingMode")

                

                mdptsInit, center = run_face_tracking(frame1)
                print(mdptsInit)

                #determines direction of calibration
                directions = direction(mdptsInit, center)
                session.direction = directions

                #calibration was pressed, ready to send to arduino
                session.calibrateR = True


                print(direction)

                #sleeps in order to let the motors move
                time.sleep(6)
                frame2_raw = sock.receive()

                try:
                    frame2 = json.loads(frame2_raw)
                except Exception as e:
                    print(e)

                frame2 = frame2.get("image")

                #strips
                if "," in frame2:
                    frame2 = frame2.split(",")[1]

                frame2 = base64.b64decode(frame2)
                
                mdptsFinal, center = run_face_tracking(frame2)


                try:
                #determines the conversion factor for px/degrees(probably won't be different but it could be)
                    conversionX = abs((mdptsFinal[0][0] - mdptsInit[0][0])/calibrationDegrees)
                    conversionY = abs((mdptsFinal[0][1] - mdptsInit[0][1])/calibrationDegrees)
                    pxByDegrees = (conversionX+conversionY)/2
                except (IndexError) as e:
                    print(e)

                else:
                    sock.send("CalibrationComplete")
                    session.conversion = pxByDegrees
               


            #tracking
            else:
                toImage()


                try:
                    #takes a frame and detects difference between face and center. Uses motor conversion to find the motor angle required
                    session.motorData = motor_angle(frame, session.conversion)
                    session.dataReady = True
                except AttributeError:
                    print("Not Calibrated")
                

            
           
    
    if __name__ == '__main__':
        # host="0.0.0.0" opens a server up so a phone can connect over your Wi-Fi
        app.run(host="0.0.0.0", port=5555, debug=True, ssl_context="adhoc", use_reloader=False)



#second server to serve the arduino face commands
def arduino_server():
    app = Flask(__name__)
    sock = Sock(app)

    @sock.route('/stream')
    def stream(ws):
        while True:

            if session.clickedCal == True:
                calData = {"move" : 90}
                ws.send(json.dumps(calData))
                session.clickedCal = False


            if session.calibrateR == True:
                calData = {
                    "type" : "calibration",
                    "calibrationLR" : session.direction[0],
                    "calibrationUD" : session.direction[1],
                    "degrees" : calibrationDegrees,
                    "facingMode" : session.facingMode
                    
                }


                time.sleep(1)

                ws.send(json.dumps(calData))
                print("Dumped!")
                session.calibrateR = False



            if session.dataReady == True:
                try:
                    data = {"type" : "tracking",
                            "xMotor" : session.motorData[0], 
                            "yMotor" : session.motorData[1]}
                except Exception as e:
                    ...
                
                ws.send(json.dumps(data))

                session.dataReady = False
            #so doesn't starve cpu
            time.sleep(0.01)

    
    app.run(host="0.0.0.0", port=5556, use_reloader=False)  # no ssl_context


        
thread1 = threading.Thread(target=main_app_server)
thread2 = threading.Thread(target=arduino_server)

thread1.start()
thread2.start()



