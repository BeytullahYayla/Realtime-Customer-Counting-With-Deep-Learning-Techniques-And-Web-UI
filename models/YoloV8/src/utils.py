import cv2
import random
import numpy as np
import configparser
color_dict = {0: (0, 0, 255),  # Grup için kırmızı
              1: (255, 0, 0)}  # Person için mavi

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]

def overlap(p_bbox, r_bbox):
    xA = max(p_bbox[0], r_bbox[0])
    yA = max(p_bbox[1], r_bbox[1])
    xB = min(p_bbox[2], r_bbox[2])
    yB = min(p_bbox[3], r_bbox[3])
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (p_bbox[2] - p_bbox[0] + 1) * (p_bbox[3] - p_bbox[1] + 1)
    overlap = interArea / boxAArea
    return overlap

# def draw_line_and_area(frame):
    

def draw_info(frame, track_id, p_bbox, classification_result=None):
    # Create the text to display, including the classification result if available
    res_text = f"Tid:{track_id}"
    class_text = f"Class:{classification_result}" if classification_result else ""
    
    # Adjust font scale and thickness for smaller text
    font_scale = 0.75
    thickness = 1
    
    # Calculate text sizes
    text_size_res, _ = cv2.getTextSize(res_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    tw_res, th_res = text_size_res
    text_size_class, _ = cv2.getTextSize(class_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    tw_class, th_class = text_size_class
    
    # Use white color for the text
    text_color = (255, 255, 255)  # White
    # Use green color for the background
    bg_color = (0, 170, 0)  # Green
    
    # Position for the track ID text
    res_text_pos = (p_bbox[0] - 5, p_bbox[1] - 10)
    # Position for the classification text below the track ID text
    class_text_pos = (p_bbox[0] - 5, p_bbox[1] + 20)
    
    # Calculate the width of the background rectangle
    max_text_width = max(tw_res, tw_class)
    
    # Draw the background rectangle for track ID text
    cv2.rectangle(frame, 
                  (res_text_pos[0], res_text_pos[1] - th_res - 5), 
                  (res_text_pos[0] + max_text_width + 10, res_text_pos[1] + 5), 
                  bg_color, 
                  cv2.FILLED)
    
    # Draw the track ID text
    cv2.putText(frame, res_text, res_text_pos, cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, text_color, thickness, cv2.LINE_AA)

    if class_text:
        # Draw the background rectangle for classification text
        cv2.rectangle(frame, 
                      (class_text_pos[0], class_text_pos[1] - th_class - 5), 
                      (class_text_pos[0] + max_text_width + 10, class_text_pos[1] + 5), 
                      bg_color, 
                      cv2.FILLED)
        
        # Draw the classification text
        cv2.putText(frame, class_text, class_text_pos, cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, text_color, thickness, cv2.LINE_AA)

       


def return_frame_with_count_info(frame,person_count:int,fps):
    text = f"Person: {person_count}"
    text_fps=f"Fps: {fps}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 30)  
    org_fps=(10,70)
    fontScale = 1
    color = (255, 255, 255)  
    thickness = 2 
    frame_with_text = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    frame_with_text = cv2.putText(frame_with_text,text_fps,org_fps,font,fontScale,color,thickness,cv2.LINE_AA)
    return frame_with_text
# Function for bounding box and ID annotation.
def annotate(tracks, frame, resized_frame, frame_width, frame_height):
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        track_class = track.det_class
        x1, y1, x2, y2 = track.to_ltrb()
        p1 = (int(x1/resized_frame.shape[1]*frame_width), int(y1/resized_frame.shape[0]*frame_height))
        p2 = (int(x2/resized_frame.shape[1]*frame_width), int(y2/resized_frame.shape[0]*frame_height))
        # Annotate boxes.
        color =(0,255,0)
        cv2.rectangle(
            frame,
            p1,
            p2,
            color=(int(color[0]), int(color[1]), int(color[2])),
            thickness=2
        )
        # Annotate ID.
        cv2.putText(
            frame, f"ID: {track_id}",
            (p1[0], p1[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
            lineType=cv2.LINE_AA
        )
    return frame
def convert_detections(yolo_detections, threshold):
    """
    Convert YOLOv8 detections to Deep SORT format.
    
    Parameters
    ----------
    yolo_detections : list
        List of detections from YOLOv8.
    threshold : float
        Score threshold to filter out detections.
    classes : list of int
        List of class IDs to track.
    
    Returns
    -------
    list
        List of detections in Deep SORT format: [x1, y1, x2, y2, score]
    """
    detections = []

    for i in range(len(yolo_detections)):
        box = yolo_detections.boxes[i]  # Get the i-th detected box
        clsID = int(box.cls.cpu().numpy()[0])  # Get the class ID
        conf = box.conf.cpu().numpy()[0]  # Get the confidence score
        bb = box.xyxy.cpu().numpy()[0]  # Get the bounding box coordinates

        # Only consider detections with a confidence score above the threshold
        if conf > threshold:
            x1 = int(bb[0])
            y1 = int(bb[1])
            x2 = int(bb[2])
            y2 = int(bb[3])
            width = x2 - x1
            height = y2 - y1
            
            # Append the detection in the required format
            detections.append(([
                x1, y1, width, height], conf, clsID
            ))
            
        return detections


def save_classification_results(cropped_frame,i):
    image_path=f"cropped\\out_cropped{i}.png"
    cv2.imwrite(image_path,cropped_frame)
def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    stores = {}
    for section in config.sections():
        stores[section] = {
            'store_name':config.get(section,"store_name"),
            'x1': config.getint(section, 'x1'),
            'y1': config.getint(section, 'y1'),
            'x2': config.getint(section, 'x2'),
            'y2': config.getint(section, 'y2')
        }
    return stores


def check_store_name(init_dict:dict,db):
    for key,param in init_dict.items():
        db.update_store_info(param["store_name"])
        
            