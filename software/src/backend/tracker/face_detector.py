from pathlib import Path
import cv2
from ultralytics import YOLO
import numpy as np
import sys




class Size:
    def __init__(self):
        self.size = None

    def get(self):
        return self.size

    def set(self, size):
        self.size = size


size = Size()

path = Path(__file__).resolve().parent.parent.parent.parent / "src/models/yolov12n-face.pt"


#conversion in px/degrees so px cancels out
def motor_angle(img, conversion)-> tuple:
    try:
        mdpts, center = run_face_tracking(img)
        print(mdpts,center)
        x = mdpts[0][0] - center[0]
        y = mdpts[0][1] - center[1]
   

    
        return(x*(1/conversion), y*(1/conversion))
    except Exception as e:
        print(e)




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
    center = (cent_x, cent_y)   
    
    
    


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
              
        return mdpts, center

    
def main():
    ...
  

if __name__ == "__main__":
    main()