import supervision as sv
from ultralytics import YOLO 
from tqdm import tqdm
import argparse
import numpy as np

tracker = sv.ByteTrack() 
def process_video(
        source_weights_path: str, 
        source_video_path: str,
        target_video_path: str, 
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7
) -> None:
    model = YOLO(source_weights_path)       # Load YOLO model 
    classes = list(model.names.values())    # Class names 
    LINE_STARTS = sv.Point(0,500)           # Line start point for count in/out vehicle
    LINE_END = sv.Point(1800, 500)          # Line end point for count in/out vehicle
    tracker = sv.ByteTrack()                # Bytetracker instance 
    box_annotator = sv.BoundingBoxAnnotator()     # BondingBox annotator instance 
    label_annotator = sv.LabelAnnotator()         # Label annotator instance 
    frame_generator = sv.get_video_frames_generator(source_path=source_video_path) # for generating frames from video
    video_info = sv.VideoInfo.from_video_path(video_path=source_video_path)
    line_counter = sv.LineZone(start=LINE_STARTS, end = LINE_END)
    line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale= 0.5)
    ##line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=0.5)

    with sv.VideoSink(target_path=target_video_path, video_info=video_info) as sink:
        for frame in tqdm(frame_generator, total= video_info.total_frames):
            # Getting result from model
            results = model(frame, verbose=False, conf= confidence_threshold, iou = iou_threshold)[0] 
            detections = sv.Detections.from_ultralytics(results)    # Getting detections
            #Filtering classes for car and truck only instead of all COCO classes.
            detections = detections[np.where((detections.class_id==0)|(detections.class_id==1))]## person and group
            detections = tracker.update_with_detections(detections)  # Updating detection to Bytetracker
            # Annotating detection boxes
            annotated_frame = box_annotator.annotate(scene = frame.copy(), detections= detections) 

            #Prepare labels
            labels = []
            for index in range(len(detections.class_id)):
                # creating labels as per required.
                labels.append("#" + str(detections.tracker_id[index]) + " " + classes[detections.class_id[index]] + " "+ str(round(detections.confidence[index],2)) )
            
            # Line counter in/out trigger
            line_counter.trigger(detections=detections)
            # Annotating labels
            annotated_label_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
            # Annotating line labels
            line_annotate_frame = line_annotator.annotate(frame=annotated_label_frame, line_counter=line_counter)
            sink.write_frame(frame = line_annotate_frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("video processing with YOLO and ByteTrack") 
    parser.add_argument(
        "--source_weights_path",
        default="son.pt",
        help="Path to the source weights file",
        type=str
    )
    parser.add_argument(
        "--source_video_path",
        default="C:\\Users\\İbrahim ATAŞ\\Desktop\\yolov8-group-object-detection\\inference\\test_videos\\4.mp4", 
        help="Path to the source video file",
        type = str
    )
    parser.add_argument(
        "--target_video_path",
        default="output_video_byte.avi",
        help="Path to the target video file",
        type= str
    )
    parser.add_argument(
        "--confidence_threshold",
        default = 0.3,
        help= "Confidence threshold for the model",
        type=float
    )
    parser.add_argument(
        "--iou_threshold",
        default=0.7,
        help="Iou threshold for the model",
        type= float
    )
    args = parser.parse_args() 
    process_video(
        source_weights_path=args.source_weights_path, 
        source_video_path= args.source_video_path,
        target_video_path=args.target_video_path, 
        confidence_threshold=args.confidence_threshold,
        iou_threshold=args.iou_threshold
    )