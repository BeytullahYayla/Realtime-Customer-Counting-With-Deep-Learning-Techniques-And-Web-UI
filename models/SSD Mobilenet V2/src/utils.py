import cv2
import random

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


def draw_info(frame, track_id, p_bbox,class_ids):
    res_text = f"Tid:{track_id}"
    text_size, _ = cv2.getTextSize(res_text, cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.75, 1)
    tw, th = text_size
    color = (0, 0, 255) 
    ##cv2.rectangle(frame, (p_bbox[0], p_bbox[1] - th - 5), (p_bbox[0] + tw, p_bbox[1]), color, -1)  # Metin arka planı
    cv2.putText(frame, res_text, (p_bbox[0]-5, p_bbox[1]-5), cv2.FONT_HERSHEY_SIMPLEX,
        0.50, (0, 0, 0), 1, cv2.LINE_AA)
