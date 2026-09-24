#takes json payload and gets image
import base64

def toImage(frame):
    try:
        #extracts image from the dict
        frame = frame.get("image")
        #strips
        if "," in frame:
            frame = frame.split(",")[1]

        #to bytes
        frame = base64.b64decode(frame)
        return frame
    except Exception as e:
        print(e)
        return 0