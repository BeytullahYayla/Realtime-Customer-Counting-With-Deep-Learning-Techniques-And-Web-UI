from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.tracker import Tracker
from deep_sort.tools import generate_detections
from deep_sort.deep_sort.detection import Detection
import numpy as np
import time


class DeepSortTracker:
        def __init__(self, encoder_model_path):
                self.max_cosine_distance = 0.4
                self.nn_budget = None
                self.encoder_model_path = encoder_model_path

                self.metric = nn_matching.NearestNeighborDistanceMetric(
                        "cosine", self.max_cosine_distance, self.nn_budget)

                self.tracker = Tracker(self.metric)
                self.encoder = generate_detections.create_box_encoder(self.encoder_model_path, 
                                                                      batch_size=1)
                

        def update(self, frame, detections):
                if len(detections) == 0:
                        self.tracker.predict()
                        self.tracker.update([])  
                        self.update_tracks()
                        return
                
               
                bboxes = np.asarray([d[:-2] for d in detections])
                
                bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
                scores = [d[-2] for d in detections]
                class_ids=[d[-1]for d in detections]
               
                features = self.encoder(frame, bboxes)
                dets = []
                for bbox_id, bbox in enumerate(bboxes):
                        dets.append(Detection(bbox, scores[bbox_id], features[bbox_id]))
                self.tracker.predict()
                self.tracker.update(dets)
                return self.update_tracks()
        
        def update_tracks(self):
                tracks = []
                deleted_tracks = []
                for track in self.tracker.tracks:
                        if not track.is_confirmed() or track.time_since_update > 1:
                                deleted_tracks.append(track.track_id)
                                continue
                        bbox = track.to_tlbr()
                        id = track.track_id
                        tracks.append(Track(id, bbox))
                self.tracks = tracks
                return deleted_tracks


class Track:
    track_id = None
    bbox = None

    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox
       
