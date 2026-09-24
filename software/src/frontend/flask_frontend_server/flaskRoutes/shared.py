#all shared variables between routes



#constant motor degrees/second(rounded from specs)
dgPerSec = 355

currentMotorAngles = [90, 90]

previousMotorAngles = [90, 90]

#check if calibration button was clicked
clickedCal = False

#checked if if start calibration was clicked
calibrateR = False

#variable for conversion factor of px/degrees
pxByDegrees = 0


#see if motor is ready to be sent off for calibration
calibrationMotorsReady = 0