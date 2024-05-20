import torch
import cv2
import os
import time
import argparse
import numpy as np

from deep_sort_realtime.deepsort_tracker import DeepSort
from utils import convert_detections,return_frame_with_count_info
from coco_classes import COCO_91_CLASSES
from ultralytics import YOLO


def argparser():
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        default='C:\\Users\\MSI\\Desktop\\Koçtaş\\test_videos\\test7.mp4',
        help='path to input video',
    )
    parser.add_argument(
        '--imgsz',
        default=640,
        help='image resize, 640 will resize images to 640x640',
        type=int
    )
    parser.add_argument(
        '--model',
        default='last.pt',
        help='path to YOLOv8 model file'
    )
    parser.add_argument(
        '--threshold',
        default=0.6,
        help='score threshold to filter out detections',
        type=float
    )
    parser.add_argument(
        '--embedder',
        default='clip_ViT-B/32',
        help='type of feature extractor to use',
        choices=[
            "mobilenet",
            "torchreid",
            "clip_RN50",
            "clip_RN101",
            "clip_RN50x4",
            "clip_RN50x16",
            "clip_ViT-B/32",
            "clip_ViT-B/16"
        ]
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='visualize results in real-time on screen'
    )
    parser.add_argument(
        '--cls',
        nargs='+',
        default=[1],
        help='which classes to track',
        type=int
    )
    args = parser.parse_args()
    return args
def get_video_writer(filename, frame_width, frame_height, frame_fps):
    # Uzantıya göre doğru codec ve uzantıyı seç
    ext = os.path.splitext(filename)[1]
    if ext.lower() == '.mp4':
        fourcc = 'mp4v'
    elif ext.lower() == '.avi':
        fourcc = 'XVID'
    else:
        raise ValueError("Unsupported file extension. Use .mp4 or .avi")

    # VideoWriter nesnesini oluştur ve döndür
    return cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*fourcc), frame_fps, (frame_width, frame_height))


if __name__=="__main__":
    
    args=argparser()
    np.random.seed(42)

    OUT_DIR = 'outputs'
    os.makedirs(OUT_DIR, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    COLORS = np.random.randint(0, 255, size=(len(COCO_91_CLASSES), 3))

    print(f"Tracking: {[COCO_91_CLASSES[idx] for idx in args.cls]}")
    print(f"Detector: YOLOv8")
    print(f"Re-ID embedder: {args.embedder}")


    # Load YOLOv8 model
    model = YOLO(args.model)
    # Initialize a SORT tracker object.
    tracker = DeepSort(max_age=30, embedder=args.embedder)

    VIDEO_PATH = args.input
    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_fps = int(cap.get(5))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    save_name = VIDEO_PATH.split(os.path.sep)[-1].split('.')[0]
    # Define codec and create VideoWriter object.
    out = cv2.VideoWriter(
    f"{OUT_DIR}/{save_name}_{args.model}_{args.embedder}.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'), frame_fps,
    (frame_width, frame_height)
)
 

    frame_count = 0 # To count total frames.
    total_fps = 0 # To get the final frames per second.
    
    total_person_count=0
    tracked_persons={}

    while cap.isOpened():
        # Read a frame
        ret, frame = cap.read()
        if ret:
            if args.imgsz != None:
                resized_frame = cv2.resize(frame, (args.imgsz, args.imgsz))
            else:
                resized_frame = frame
            resized_frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

            start_time = time.time()
            # Feed frame to YOLOv8 model and get detections.
            det_start_time = time.time()
            results = model(resized_frame_rgb, conf=args.threshold)
            det_end_time = time.time()

            det_fps = 1 / (det_end_time - det_start_time)
        
            # Convert detections to Deep SORT format.
            detections = convert_detections(results[0], args.threshold)
            # Iterate over the detected boxes
            for i in range(len(results[0])):
                box = results[0].boxes[i]  # Get the i-th detected box
                clsID = int(box.cls.cpu().numpy()[0])  # Get the class ID
                conf = box.conf.cpu().numpy()[0]  # Get the confidence score
                bb = box.xyxy.cpu().numpy()[0]  # Get the bounding box coordinates

                # Only consider detections with a confidence score above the threshold
                if conf > args.threshold:
                    x1 = int(bb[0])
                    y1 = int(bb[1])
                    x2 = int(bb[2])
                    y2 = int(bb[3])
                    cv2.rectangle(resized_frame,(x1,y1),(x2,y2),(0,255,0),2)
        
            
            # Update tracker with detections.
            track_start_time = time.time()
            
            if detections is not None:
                
                tracks = tracker.update_tracks(detections, frame=resized_frame)
                for track in tracks:
                    track_id = track.track_id
                    bbox = track.to_tlbr()
                    x_center=int((bbox[0]+bbox[2])/2)
                    y_center=int((bbox[1]+bbox[3])/2)
                    
                    if track_id  not in tracked_persons:
                        if y_center>160:
                            tracked_persons[track_id]=True
                            total_person_count+=1
                        
                      # Get the bounding box coordinates [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
                    
                    cv2.putText(
                        resized_frame,
                        f"Track ID: {track_id}",
                        (int(bbox[0]), int(bbox[1]) - 10),  # Position the text slightly above the top-left corner of the bounding box
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(0, 255, 0),  # Green color for the text
                        thickness=2,
                        lineType=cv2.LINE_AA
                    )
                    
                
                
                track_end_time = time.time()
                track_fps = 1 / (track_end_time - track_start_time)

                end_time = time.time()
                fps = 1 / (end_time - start_time)
            # Add `fps` to `total_fps`.
                total_fps += fps
            # Increment frame count.
                frame_count += 1

                print(f"Frame {frame_count}/{frames}",
                    f"Detection FPS: {det_fps:.1f},",
                    f"Tracking FPS: {track_fps:.1f}, Total FPS: {fps:.1f}")
           
                
            out.write(resized_frame)
            if args.show:
                # Display or save output frame.
                cv2.imshow("Output", resized_frame)
                # Press q to quit.
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        else:
            break
        
    # Release resources.
    print(total_person_count)
    cap.release()
    cv2.destroyAllWindows()
    out.release()
