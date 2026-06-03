import cv2
from ultralytics import YOLO
from pathlib import Path



def run_face_tracking(capture_num):
    
    path = Path(__file__).resolve().parent.parent / "src/models/yolov12n-face.pt"
    print(path)
    # load model
    model = YOLO(path)

    #instantiate capture obj with a parameter of camera "number"
    cap = cv2.VideoCapture(1)



    while True:
        #cap.read takes the image from the webcam and returns numpy array.
        ret, image = cap.read()
        print(image)

        #flips image so camera movement is not inverted
        image = cv2.flip(image, 1)

        #uses yolo's __call__ method to run the model on the image
        mod = model(image, stream=True)

        # i being number of faces
        for i in mod:
            boxes = i.boxes

            for box in boxes:
                #gets "coodinates" from the Box object
        
                #unpacking an array
                x1, y1, x2, y2 = box.xyxy[0]
                
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                #finds center point, using midpoint formula
                cx1 = (x1+x2)/2
                cy1 = (y1+y2)/2

                #draws bounding box right on image
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 10)
                cv2.circle(image, (int(cx1),int(cy1)), 5, (0,0,0), 10)       

                
            #shows in "cam" window
            cv2.imshow("cam",image)

        #whole process takes ~1ms, when q is pressed, the loop is broken
        if cv2.waitKey(1) == ord("q"):
            break

    #cleaning
    cap.release
    cv2.destroyAllWindows()




if __name__ == "__main__":
    run_face_tracking(1)