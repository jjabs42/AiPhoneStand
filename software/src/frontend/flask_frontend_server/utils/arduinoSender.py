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
        shared.previousMotorAngles = shared.currentMotorAngles
        ws.send(json.dumps({
            "xMotor" : shared.currentMotorAngles[0] + motorData[0],
            "yMotor" : shared.currentMotorAngles[1] + motorData[1]
            }))

        shared.currentMotorAngles[0] = shared.currentMotorAngles[0] + motorData[0]
        shared.currentMotorAngles[1] = shared.currentMotorAngles[1] + motorData[1]

def sendTo(motorData: list):
    if ws:
        shared.previousMotorAngles = shared.currentMotorAngles
        ws.send(json.dumps({
            "xMotor" : motorData[0], 
            "yMotor" : motorData[1]
            }))
        shared.currentMotorAngles[0] = motorData[0]
        shared.currentMotorAngles[1] = motorData[1]
        





