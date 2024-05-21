import torch
import cv2
import os
import time
import argparse
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort
from tracker import Tracker
from utils import convert_detections, return_frame_with_count_info, annotate, draw_info
from classification import CustomerClassification
from coco_classes import COCO_91_CLASSES
from ultralytics import YOLO


    
""" Track id değişimi için resimleri karşılaştırma

"""
def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
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
        default='best.pt',
        help='path to YOLOv8 model file'
    )
    parser.add_argument(
        '--threshold',
        default=0.7,
        help='score threshold to filter out detections',
        type=float
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
    parser.add_argument(
        "--tracking",
        type=int,
        default=0
    )
    args = parser.parse_args()
    return args

def save_video(frames, fps, size, output_path):
    # Determine the codec based on the file extension
    if output_path.endswith('.avi'):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'XVID' codec for .avi files
    elif output_path.endswith('.mp4'):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'mp4v' codec for .mp4 files
    else:
        raise ValueError("Unsupported file format. Use .avi or .mp4")

    out = cv2.VideoWriter(output_path, fourcc, fps, size)
    for frame in frames:
        out.write(frame)
    out.release()
def save_classification_results(cropped_frame,i):
    image_path=f"cropped\\out_cropped{i}.png"
    cv2.imwrite(image_path,cropped_frame)
    
if __name__ == "__main__":
    args = argparser()
    np.random.seed(42)

    OUT_DIR = 'outputs'
    os.makedirs(OUT_DIR, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    COLORS = np.random.randint(0, 255, size=(len(COCO_91_CLASSES), 3))

    tracked_persons = {}

    print(f"Tracking: {[COCO_91_CLASSES[idx] for idx in args.cls]}")
    print(f"Detector: YOLOv8")


    # Load YOLOv8 model
    model = YOLO(args.model)
    # Initialize a SORT tracker object.
    tracker_without_gpu = Tracker()
    classiffier=CustomerClassification('models\\weights.h5')

    VIDEO_PATH = args.input
    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_fps = int(cap.get(5))
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    save_name = VIDEO_PATH.split(os.path.sep)[-1].split('.')[0]

    output_path = os.path.join(OUT_DIR, f"{save_name}_output.avi")
    processed_frames = []

    frame_count = 0  # To count total frames.
    total_fps = 0  # To get the final frames per second.

    total_person_count = 0
    tracked_persons = {}
    classification_results=[]
    
      # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs such as 'MJPG', 'X264', etc.
    output_video_path = 'output_video.avi'  # Choose the desired output video file path
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (640, 640))  # Use the same fps as input video
   
    while cap.isOpened():
        # Read a frame
        ret, frame = cap.read()
        if ret:
            if args.imgsz is not None:
                resized_frame = cv2.resize(frame, (args.imgsz, args.imgsz))
                resized_frame_empty=resized_frame.copy()
            else:
                resized_frame = frame
            
            resized_frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            cv2.line(resized_frame,(0,160),(640,160),(0,255,0),1)
            start_time = time.time()
            # Feed frame to YOLOv8 model and get detections.
            results = model(resized_frame_rgb, conf=args.threshold)

            # Convert detections to Deep SORT format.
            detections_gpu_converted = convert_detections(results[0], args.threshold)
            dets = []
            # Iterate over the detected boxes
            for i in range(len(results[0])):
                box = results[0].boxes[i]  # Get the i-th detected box
                clsID = int(box.cls.cpu().numpy()[0])  # Get the class ID
                conf = box.conf.cpu().numpy()[0]  # Get the confidence score
                bb = box.xyxy.cpu().numpy()[0]  # Get the bounding box coordinates

                # Only consider detections with a confidence score above the threshold
                x1 = int(bb[0])
                y1 = int(bb[1])
                x2 = int(bb[2])
                y2 = int(bb[3])
                dets.append([x1, y1, x2, y2, conf])
                cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            if args.tracking == 1:
                tracker_without_gpu.update(resized_frame, dets)
                for track in tracker_without_gpu.tracks:
                    p_bbox = list(map(int, track.bbox))
                    x1, y1, x2, y2 = p_bbox
                    track_id = track.track_id
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    draw_info(resized_frame, track_id, p_bbox)
                    if track_id not in tracked_persons:  # Eğer takip edilen kişi takip edilmiyorsa
                        if center_y >= 160:  # Eğer kişi çizgiyi geçtiyse
                            tracked_persons[track_id] = True  # Takip edildi olarak işaretle
                            cropped_image=resized_frame_empty[y1:y2,x1:x2]
                            
                            save_classification_results(cropped_image,track_id)
                            resized_image=cv2.resize(cropped_image,(224,224))
                            result=classiffier.classification(resized_image)
                            classification_results.append(result)
                            total_person_count += 1  # İnsan sayısını artır

                        

            processed_frames.append(resized_frame)
            end_time = time.time()  # İşlem bitiş zamanını kaydet
            elapsed_time = end_time - start_time  # Geçen süreyi hesapla
            fps = 1 / elapsed_time  # FPS değerini hesapla
            fps = "{:.2f}".format(fps)
            draw_frame_text=return_frame_with_count_info(resized_frame,total_person_count,fps)
            out.write(draw_frame_text)
            if args.show:
                # Display output frame.
                cv2.imshow("Output", resized_frame)
                # Press q to quit.
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        else:
            break

    # Save the video with processed frames
    # save_video(processed_frames, frame_fps, (frame_width, frame_height), output_path)

    # Release resources.
    print(total_person_count)
    print(tracked_persons)
    print(classification_results)
    cap.release()
    cv2.destroyAllWindows()
    out.release()
