# import necessary modules
import cv2
import numpy as np
# import the yolo detector file
from . import YoloDetector
from core.models import video

def detect(selected,files):
    # read the default classes for the yolo model
    with open("data\coco.names", 'r') as f:
        classes = [w.strip() for w in f.readlines()]
    print("Default classes: \n")
    for n, cls in enumerate(classes):
        print("%d. %s" % (n+1, cls))
    # select specific classes that you want to detect out of the 80 and assign a color to each detection
    # initialize the detector with the paths to cfg, weights, and the list of classes
    detector = YoloDetector.YoloDetector("data\yolov3-tiny.cfg", "data\yolov3-tiny.weights", classes)
    # initialize video stream
    video="media/"+str(files.video)
    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    
    size = (frame_width, frame_height) 
    
    # Below VideoWriter object will create 
    # a frame of above defined The output  
    # is stored in 'filename.avi' file. 
    result = cv2.VideoWriter('static/videos/output.mp4',  
                            cv2.VideoWriter_fourcc(*'mp4v'), 
                            20, size) 
    # read first frame
    ret, frame = cap.read()
    # loop to read frames and update window
    while ret:
        # this returns detections in the format {cls_1:[(top_left_x, top_left_y, top_right_x, top_right_y), ..],
        #                                        cls_4:[], ..}
        # Note: you can change the file as per your requirement if necessary
        detections = detector.detect(frame)
        # loop over the selected items and check if it exists in the detected items, if it exists loop over all the items of the specific class
        # and draw rectangles and put a label in the defined color
        for cls, color in selected.items():
            if cls in detections:
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
        # display the detections
        result.write(frame)
        # wait for key press
        key_press = cv2.waitKey(1) & 0xff
        # exit loop if q or on reaching EOF
        if key_press == ord('q'):
            break
        ret, frame = cap.read()
    # release resources
    result.release()

    cap.release()
    
    
    # destroy window
    cv2.destroyAllWindows()
    return result

