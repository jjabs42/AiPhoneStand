
#determines if calibration should move x degrees right or x degrees left(up or down too), returning the bottom motor first
def direction(mdpts, center)->tuple:
    print(mdpts,center)
    movements = []
    if center[0] - mdpts[0][0] >= 0:
        movements.append("l")
    else:
        movements.append("r")

    if center[1] - mdpts[0][1] >= 0:
        movements.append("d")
    else:
        movements.append("u")

    return movements

#this function determines based off direction, 
def CalibrationAngles():
    ...