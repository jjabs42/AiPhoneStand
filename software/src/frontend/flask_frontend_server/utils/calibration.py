import json
from .imaging import toImage
from ....backend.tracker import run_face_tracking
import time
from .arduinoSender import sendAmount, sendTo

#determines if calibration should move x degrees right or x degrees left(up or down too), returning the bottom motor first...Always starting at 90
def motorMove(mdpts, center, facingMode, degreesMoved)->tuple:
    print(mdpts,center)
    movements = []
    if facingMode == "user":
        if center[0] - mdpts[0][0] >= 0:
            movements.append(-degreesMoved)
        else:
            movements.append(degreesMoved)

        if center[1] - mdpts[0][1] >= 0:
            movements.append(-degreesMoved)
        else:
            movements.append(degreesMoved)

    elif facingMode == "environment":
        ...
    return movements


    



#this function runs Calibration and returns the conversion factor
def calibrate(sock, calibrationDegrees):
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
    directions = motorMove(mdptsInit, center, facingMode=facingMode, degreesMoved=calibrationDegrees)
    directions = list(directions)

    #sends motor commands
    sendAmount(directions)




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
    #determines the conversion factor for px/degrees(probably won't be different but it could be because of distortion)
        conversionX = abs((mdptsFinal[0][0] - mdptsInit[0][0])/calibrationDegrees)
        conversionY = abs((mdptsFinal[0][1] - mdptsInit[0][1])/calibrationDegrees)
        pxByDegrees = (conversionX+conversionY)/2
        
    except (IndexError) as e:
        print(e)
        sock.send("CalibrationFailed")
        sendTo([90,90])
        return 0

    else:
        sock.send("CalibrationComplete")
        sendTo([90,90])
        return pxByDegrees
        

    