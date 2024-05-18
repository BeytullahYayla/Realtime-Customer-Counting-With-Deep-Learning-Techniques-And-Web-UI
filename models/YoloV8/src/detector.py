from ultralytics import YOLO
import torch
class YOLOv8Detector:
    def __init__(self, model_path, det_thres=0.6):
        # YOLO modelini CUDA cihazına taşıma
        self.model = YOLO(model_path,"v8")
        self.det_thres = det_thres
    
    def detect(self, frame):
   
        # YOLO modelini kullanarak tespit yapma
        detect_params = self.model(source=[frame],device=0,conf=self.det_thres,save=False)
        
        # Tespitleri işleme ve uygun formata dönüştürme
        DP=detect_params[0].cpu().numpy()
        detections=[]
        if len(DP) != 0:
            for i in range(len(detect_params[0])):
                # print(i)

                boxes = detect_params[0].boxes
                box = boxes[i]  # returns one box
                clsID = box.cls.cpu().numpy()[0]
                conf = box.conf.cpu().numpy()[0]
                bb = box.xyxy.cpu().numpy()[0]
                print(bb)
                x1=int(bb[0])
                x2=int(bb[1])
                y1=int(bb[2])
                y2=int(bb[3])
                
                
                detections.append([x1,x2,y1,y2,clsID,conf])
                
        
        return detections,detect_params
