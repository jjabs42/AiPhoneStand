import json
from . import shared
from ....backend.tracker import motor_angle
from ..utils import calibrate
from ..utils import sendTo, sendAmount
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
                print(f"Json failed{e}")

            
            if jsonData.get("CalibrationInitiated") == True:
                sendTo([90,90])



            
            #saying that if the thing we want to do is calibrate, then we calibrate
            elif jsonData.get("action") == "CalibrationActive":
                calibrate(sock, calibrationDegrees)
                
                


            #tracking
            else:
                if shared.pxByDegrees == 0:
                    print("Please Calibrate")
                    sock.send("CalibrationFailed")
                    

                else:
                    try:
                        data = toImage(jsonData)
                        #takes a frame and detects difference between face and center. Uses motor conversion to find the motor angle required
                        motorData = motor_angle(data, shared.pxByDegrees)
                        print(motorData)
                        sendAmount(motorData)
                    except AttributeError:
                        print("Not Calibrated")
                    
