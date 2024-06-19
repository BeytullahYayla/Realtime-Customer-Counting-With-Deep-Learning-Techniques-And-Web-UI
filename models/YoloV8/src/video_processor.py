
import cv2
import numpy as np
import time
import torch
from PyQt5.QtCore import QThread
from ultralytics import YOLO
from database import CustomerCountingDatabase
from tracker import Tracker
from utils import  return_frame_with_count_info, draw_info, check_store_name, read_ini_file
from classification import CustomerClassification
from coco_classes import COCO_91_CLASSES
from constants import *

class VideoProcessor(QThread):
    def __init__(self, video_path, imgsz, model_path, threshold, classes, store_name, tracking, show):
        super().__init__()
        self.video_path = video_path
        self.imgsz = imgsz
        self.model_path = model_path
        self.threshold = threshold
        self.classes = classes
        self.store_name = store_name
        self.tracking = tracking
        self.show = show
        self.running = False

    def run(self):
        self.running = True

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tracked_persons = {}
        
        # Read ini file
        init_dict = read_ini_file(CONFIG_DIR)
        line_configs = init_dict[self.store_name]
        
        # Initialize Db
        db = CustomerCountingDatabase(
            host=HOST,
            user=USER,
            password=PASSWORD,
            db_name=DB_NAME,
            port=PORT
        )
        
        # Add database to store name if it is not exist!
        check_store_name(init_dict, db)
        
        # Load YOLOv8 model
        model = YOLO(self.model_path)
        
        # Initialize a SORT tracker object.
        tracker_without_gpu = Tracker()
        
        # Load classification model
        classifier = CustomerClassification(CLASSIFICATION_MODEL_DIR)

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        total_person_count = 0
        classification_results = {}
        classification_count_results = {'Woman': 0, 'Man': 0, 'Kid': 0, 'Employee': 0, 'Staff': 0}
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if self.imgsz is not None:
                resized_frame = cv2.resize(frame, (self.imgsz, self.imgsz))
            else:
                resized_frame = frame
            
            resized_frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            if self.tracking==1:
                
                cv2.line(resized_frame, (line_configs["x1"], line_configs["y1"]), (line_configs["x2"], line_configs["y2"]), (255, 0, 0), 2)
            
            start_time = time.time()
            results = model(resized_frame_rgb, conf=self.threshold)
            
            dets = []
            for result in results[0].boxes:
                if result.conf >= self.threshold:
                    x1, y1, x2, y2 = result.xyxy.cpu().numpy().astype(int).flatten()
                    cv2.rectangle(resized_frame,(x1,y1),(x2,y2),(0,255,0),2)
                    conf = result.conf.item()
                    dets.append([x1, y1, x2, y2, conf])

            if self.tracking:
                tracker_without_gpu.update(resized_frame, dets)
                for track in tracker_without_gpu.tracks:
                    x1, y1, x2, y2 = map(int, track.bbox)
                    track_id = track.track_id
                    center_y = int((y1 + y2) / 2)

                    if track_id not in tracked_persons and center_y >= line_configs["y1"]:
                        tracked_persons[track_id] = True
                        cropped_image = resized_frame[y1:y2, x1:x2]
                        resized_image = cv2.resize(cropped_image, (224, 224))
                        result = classifier.classification(resized_image)
                        classification_count_results[result] += 1
                        total_person_count += 1
                        db.update_count_info(
                            store_name=self.store_name,
                            man_count=classification_count_results["Man"],
                            woman_count=classification_count_results["Woman"],
                            kid_count=classification_count_results["Kid"],
                            staff_count=classification_count_results["Staff"],
                            employee_count=classification_count_results["Employee"],
                            total_count=total_person_count
                        )
                        classification_results[track_id] = result

                    draw_info(resized_frame, track_id, [x1, y1, x2, y2], classification_results.get(track_id))
            
            elapsed_time = time.time() - start_time
            fps = 1 / elapsed_time if elapsed_time > 0 else 0
            draw_frame_text = return_frame_with_count_info(resized_frame, total_person_count, f"{fps:.2f}")

           
            
            # Display the frame using OpenCV
            cv2.imshow("Output", draw_frame_text)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        db.close()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()