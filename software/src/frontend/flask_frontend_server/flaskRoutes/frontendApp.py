import json
import shared
from ....backend.tracker import run_face_tracking, motor_angle
from ..utils import direction
import time
import base64
from ..utils import toImage

#number of degrees to move the motors for calibration
calibrationDegrees = 25

#just put the sock object into here to create a session
def registerSocket(sock):
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

            
            if jsonData.get("CalibrationInitiated") == True:
                shared.clickedCal = True


            
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

                frame1 = toImage(frame1)

                

                mdptsInit, center = run_face_tracking(frame1)

                #determines direction of calibration
                directions = direction(mdptsInit, center)


                #sleeps in order to let the motors move
                time.sleep(6)
                frame2_raw = sock.receive()

                try:
                    frame2 = json.loads(frame2_raw)
                except Exception as e:
                    print(e)

                frame2 = toImage(frame2)
                
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
                
