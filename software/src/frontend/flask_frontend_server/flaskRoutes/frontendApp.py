import json
from . import shared
from ....backend.tracker import run_face_tracking, motor_angle
from ..utils import calibrate, toImage



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
                pxByDegrees = calibrate(sock, calibrationDegrees)
                shared.pxByDegrees = pxByDegrees
                


            #tracking
            else:
                if shared.pxByDegrees == 0:
                    raise ValueError("Please Calibrate")


                try:
                    #takes a frame and detects difference between face and center. Uses motor conversion to find the motor angle required
                    motorData = motor_angle(data, shared.pxByDegrees)
                    shared.dataReady = True
                except AttributeError:
                    print("Not Calibrated")
                
