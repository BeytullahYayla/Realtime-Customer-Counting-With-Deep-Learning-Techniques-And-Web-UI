import random
import cv2
import numpy as np
import time
import argparse
from ultralytics import YOLO
from detector import YOLOv8Detector
from tracker import DeepSortTracker
from utils import draw_info, overlap
import matplotlib.pyplot as plt
import tensorflow as tf


def parse_args():
    parser = argparse.ArgumentParser(description="Object detection and tracking script.")
    parser.add_argument("--video_path", type=str, default="C:\\Users\\MSI\\Desktop\\Koçtaş\\test_videos\\test5.avi",
                        help="Path to the input video file.")
    parser.add_argument("--model_path", type=str, default="last.pt",
                        help="Path to the YOLOv8 model file.")
    parser.add_argument("--group",type=bool,default=0)
    
    return parser.parse_args()
def return_frame_with_count_info(frame,person_count:int,fps):
    # Metni ekleyin
    
    text = f"Person: {person_count}"
    text_fps=f"Fps: {fps}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 30)  # Metnin başlangıç koordinatları
    org_fps=(10,70)
    fontScale = 1
    color = (255, 255, 255)  # Beyaz renk
    thickness = 2  # Yazı kalınlığı
    frame_with_text = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    frame_with_text=cv2.putText(frame_with_text,text_fps,org_fps,font,fontScale,color,thickness,cv2.LINE_AA)
    return frame_with_text

def get_label_name(index:int):
    LABELS={
        0:"Employee",
        1:"Kid",
        2:"Man",
        3:"Staff",
        4:"Woman"
    }
    return LABELS[index]
# Test veri setini yükleyip ön işleme yapma fonksiyonu
def load_and_preprocess_image(img):
    img = cv2.resize(img, (224, 224))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = img / 255.0  # normalize to [0,1] range
    img_array = np.expand_dims(img, axis=0)
    return img_array

def classification(image,model):
    preprocessed_img=load_and_preprocess_image(image)
    y_pred=model.predict(preprocessed_img)
    y_pred=np.argmax(y_pred,axis=1)
    print(y_pred)
    return get_label_name(y_pred[0])


if __name__=='__main__':
    
    # opening the file in read mode
    my_file = open("class.txt", "r")
    # reading the file
    data = my_file.read()
    # replacing end splitting the text | when newline ('\n') is seen.
    class_list = data.split("\n")
    my_file.close()
    
    person_count=0
    group_count=0
    tracked_people={}
    tracked_group={}

    classification_result_list=[]
    tracker = DeepSortTracker("models/mars-small128.pb")
    # Model yükleme
    # strategy = tf.distribute.MirroredStrategy()
    # with strategy.scope():
   
    #     classification_model=tf.keras.saving.load_model('C:\\Users\\MSI\\Documents\\GitHub\\InsightTrack-AI-Powered-Demographic-Analysis-and-Counting-for-Public-Spaces-main\\models\\SSD Mobilenet V2\\src\\models\\weights.h5')


    # Generate random colors for class list
    detection_colors = []
    for i in range(len(class_list)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_colors.append((b, g, r))

    # load a pretrained YOLOv8n model
    print("Started...")
    model = YOLO("last.pt", "v8")
    print("Model is loaded.")

    # Vals to resize video frames
    frame_wid = 640
    frame_hyt = 640

    cap = cv2.VideoCapture("C:\\Users\\MSI\\Desktop\\Koçtaş\\test_videos\\test1.avi")
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs such as 'MJPG', 'X264', etc.
    output_video_path = 'output_video.avi'  # Choose the desired output video file path
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (640, 640))  # Use the same fps as input video
        

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        start_time=time.time()
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        #  resize the frame | small frame optimise the run
        draw_frame = cv2.resize(frame, (frame_wid, frame_hyt))
        
        cv2.line(draw_frame,(0,160),(640,160),(0,255,0),1)
        
        draw_frame_orig=draw_frame.copy()

        # Predict on image
        detect_params = model.predict(source=[draw_frame],device=0, conf=0.8, save=False)

   
        DP = detect_params[0].cpu().numpy()

        dets=[]
        if len(DP) != 0:
            for i in range(len(detect_params[0])):
             
                boxes = detect_params[0].boxes
                box = boxes[i] 
                clsID = box.cls.cpu().numpy()[0]
                conf = box.conf.cpu().numpy()[0]
                bb = box.xyxy.cpu().numpy()[0]
                
                x1=int(bb[0])
                y1=int(bb[1])
                x2=int(bb[2])
                y2=int(bb[3])
                
                dets.append([x1,y1,x2,y2,clsID,conf])

                cv2.rectangle(
                    draw_frame,
                    (x1,y1),
                    (x2,y2),
                    detection_colors[int(clsID)],
                    3,
                )

                # Display class name and confidence
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 0.5  
                thickness = 1  
                cv2.putText(
                    draw_frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    fontScale,
                    (255, 255, 255),
                    thickness,
                )
                class_ids=[d[-1]for d in dets]
                deleted_track_ids = tracker.update(draw_frame, dets)
                for track, class_id in zip(tracker.tracks, class_ids):
                       
                                p_bbox = list(map(int, track.bbox))
                                x1, y1, x2, y2 = p_bbox
                                track_id = track.track_id
                                center_x = int((x1 + x2) / 2)
                                center_y = int((y1 + y2) / 2)
                                draw_info(draw_frame, track_id, p_bbox, class_id)
                                result_list=[]
                                if track_id not in tracked_people:  # Eğer takip edilen kişi takip edilmiyorsa
                                    if center_y >= 160:  # Eğer kişi çizgiyi geçtiyse
                                        # cropped_image=draw_frame_orig[y1:y2,x1:x2]
                                     
                                        # resized_image=cv2.resize(cropped_image,(224,224))
                                        
                                        # result=classification(cropped_image,classification_model)
                                        # # plt.imshow(cropped_image)
                                        # classification_result_list.append(result)
                                        # plt.waitforbuttonpress()
                                        tracked_people[track_id] = True  # Takip edildi olarak işaretle
                                        person_count += 1  # İnsan sayısını artır
        end_time = time.time()  # İşlem bitiş zamanını kaydet
        elapsed_time = end_time - start_time  # Geçen süreyi hesapla
        fps = 1 / elapsed_time  # FPS değerini hesapla
        fps = "{:.2f}".format(fps)
        text_fps=f"Fps: {fps}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (10, 30)  # Metnin başlangıç koordinatları
        org_fps=(10,70)
        fontScale = 1
        color = (255, 255, 255)  # Beyaz renk
        thickness = 2  # Yazı kalınlığı
        
        cv2.putText(draw_frame,text_fps,org_fps,font,fontScale,color,thickness,cv2.LINE_AA)
        print(f"fps:{fps}")
        out.write(draw_frame)
        # Display the resulting frame
        cv2.imshow("ObjectDetection", draw_frame)

        # Terminate run when "Q" pressed
        if cv2.waitKey(1) == ord("q"):
            break

    print(person_count)
    out.release()
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    