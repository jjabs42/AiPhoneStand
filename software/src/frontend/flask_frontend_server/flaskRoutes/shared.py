#all shared variables between routes

currentMotorAngles = [90, 90]

#check if calibration button was clicked
clickedCal = False

#checked if if start calibration was clicked
calibrateR = False

#variable for conversion factor of px/degrees
pxByDegrees = 0

#sees if motor angle is ready to be sent off, for tracking
dataReady = False

#see if motor is ready to be sent off for calibration
calibrationMotorsReady = 0