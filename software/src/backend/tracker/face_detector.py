from pathlib import Path
import cv2
from ultralytics import YOLO
import numpy as np
import sys


horizontal_fov = 68
vertical_fov = 51

class Size:
    def __init__(self):
        self.size = None

    def get(self):
        return self.size

    def set(self, size):
        self.size = size


size = Size()

path = Path(__file__).resolve().parent.parent.parent.parent / "src/models/yolov12n-face.pt"




#using shaky conversion factors to get angle, will use pid soon
def get_commands_simple(img):
    
    _, pts, center = run_face_tracking(img)


    #creates conversion factor in degrees/px
    h_ratio = horizontal_fov / size.get()[0] 
    v_ratio = vertical_fov / size.get()[1] 
   
    '''
    The signage (-) is meant to get the difference from the perspective of the camera/motors.
    For example, if the head moves right, the x value would be negative because the motor must move left. I also had to
    take into account the fact that the pixel coordinates start from the top left, not the middle. So that is the cause for 
    the order in which I subtract each value. The final coordinates assume that the origin is in the center of the image.
    '''

    #gets the difference between the face and the center | adding multiple faces later using averages
    try:
        x_dist = center[0]-pts[0][0]
        
        y_dist = center[1]-pts[0][1]
    except IndexError:
        return("No Face Found")

    horiz_move = x_dist * h_ratio
    vert_move = y_dist * v_ratio

    degrees_moved = (horiz_move, vert_move)

    return degrees_moved


def run_face_tracking(img):
    
    
    
    # load model
    model = YOLO(path)  
    
    image = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    #image.shape returns the height of the image and the width of the image, using to find center point
    height, width = image.shape[:2]
    
    size.set((width, height))

    print(width, height)
    #I say width is x
    
    cent_x = width/2
    cent_y = height/2

    
    
    


    #uses yolo's __call__ method to run the model on the image
    mod = model(image, stream=True)


    mdpts = []
    # i being number of faces
    for i in mod:
        boxes = i.boxes

        for box in boxes:
            #gets "coordinates" from the Box object
    
            #unpacking an array
            x1, y1, x2, y2 = box.xyxy[0]
            
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            #finds center point, using midpoint formula
            cx1 = (x1+x2)/2
            cy1 = (y1+y2)/2
            mdpts.append((cx1, cy1))

            #draws bounding box right on image
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 10)
            cv2.circle(image, (int(cx1),int(cy1)), 5, (0,0,0), 10)
            cv2.circle(image, (int(cent_x), int(cent_y)),5,(0,0,0), 10)       

            
        
        image = cv2.flip(image, 1)
        
        #remind to remove(takes time)
        success, jpgArray = cv2.imencode(".jpg", image)
        

        if success:
            jpgBytes = jpgArray.tobytes()
            #returning all 3 to display image in memory
            return jpgBytes, mdpts, (cent_x, cent_y)

    
def main():
    ...
  

if __name__ == "__main__":
    main()