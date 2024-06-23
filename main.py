from ultralytics import YOLO
import cv2
import numpy as np
import time

from sort import *
from util import *


mot_tracker = Sort()

# Load Models
coco_model = YOLO('yolov8n.pt')  
license_plate_detector = YOLO('./models/plate_detector.pt') 


# Initialize webcam capture
cap = cv2.VideoCapture(0) 

# List of vehicle classes
vehicles = [2, 3, 5, 7]

frames = []
capturing = False
start_time = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture frame from webcam. Exiting...")
        break

    if not capturing:
        # Detect license plates
        license_plates = license_plate_detector(frame)[0]
        if len(license_plates.boxes.data.tolist()) > 0:
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                
                # Crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                
                # Display captured frame with bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Start capturing frames for 3 seconds
                capturing = True
                start_time = time.time()
                frames = []

    # Capture frames for 3 seconds
    if capturing:
        current_time = time.time()
        frames.append(frame)

        # Stop capturing after 3 seconds
        if current_time - start_time >= 3:
            capturing = False
            print(f"Captured {len(frames)} frames in 3 seconds.")
            
            # Process each captured frame
            for idx, f in enumerate(frames):
                # Detect vehicles using YOLO model
                detections = coco_model(f)[0]
                detections_ = [[x1, y1, x2, y2, score] for x1, y1, x2, y2, score, class_id in detections.boxes.data.tolist() if int(class_id) in vehicles]
                
                # Tracking vehicles using SORT tracker
                track_ids = mot_tracker.update(np.asarray(detections_))
                
                # Detect license plates in the captured frame
                license_plate_in_frame = license_plate_detector(f)[0]
                
                for license_plate in license_plate_in_frame.boxes.data.tolist():  
                    x1, y1, x2, y2, score, class_id = license_plate
                    
                    # Assign license plate to the corresponding vehicle
                    xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)
         
                    # Crop license plate
                    license_plate_crop = f[int(y1):int(y2), int(x1): int(x2), :]
                        
                    # Process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                    
                    # Read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)
                    print(f"Frame {idx + 1}: Detected License Plate: {license_plate_text}")
                    
            frames = []  # Clear frames list for the next capture
            
    # Display the frame with detections
    cv2.imshow('Frame', frame)
            
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
