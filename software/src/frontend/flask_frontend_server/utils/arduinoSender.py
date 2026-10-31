import json
from ..flaskRoutes import shared
#sends cmmds to arduino
ws = None



def connect(connection):
    global ws 
    ws = connection


#parameter is a tuple of x(bottom motor), and y(top motor) commands
def sendAmount(motorData: list):
   
    if ws:
    
        try:
            ws.send(json.dumps({
                "xMotor" : int(shared.currentMotorAngles[0]) + int(motorData[0]),
                "yMotor" : int(shared.currentMotorAngles[1]) + int(motorData[1])
                }))
            shared.currentMotorAngles[0] += motorData[0]
            shared.currentMotorAngles[1] += motorData[1]
        except TypeError:
            print("No Face")

        

def sendTo(motorData: list):
    if ws:
        
        try:
            ws.send(json.dumps({
            "xMotor" : motorData[0], 
            "yMotor" : motorData[1]
            }))
            shared.currentMotorAngles[0] = motorData[0]
            shared.currentMotorAngles[1] = motorData[1]
        except TypeError:
            print("no face")
        
        





