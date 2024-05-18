import os
import argparse
import cv2
import numpy as np
import sys
import importlib.util
from tracker import Tracker
import matplotlib.pyplot as plt
import tqdm
import warnings
import time
from utils import draw_info
from configparser import ConfigParser
import matplotlib.pyplot as plt
import tensorflow as tf

warnings.filterwarnings("ignore")

def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                        required=True)
    parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                        default='detect.tflite')
    parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                        default='labelmap.txt')
    parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                        default=0.7)
    parser.add_argument('--video', help='Name of the video file',
                        default='test.mp4')
    parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                        action='store_true')
    parser.add_argument('--store',type=str,required=True)
    
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

    
if __name__=="__main__":
    
    args = parse_args()
    config=ConfigParser()
    config.read("customer_counting.ini")

    line_coords=config[args.store]
    #Constant parametersBAY
    MODEL_NAME = args.modeldir
    GRAPH_NAME = args.graph
    LABELMAP_NAME = args.labels
    VIDEO_NAME = args.video
    min_conf_threshold = float(args.threshold)
    use_TPU = args.edgetpu
    
    person_count=0
    tracked_people={}


    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    # If using Coral Edge TPU, import the load_delegate library
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
        if use_TPU:
            from tflite_runtime.interpreter import load_delegate
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        if use_TPU:
            from tensorflow.lite.python.interpreter import load_delegate

    # If using Edge TPU, assign filename for Edge TPU model
    if use_TPU:
        # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
        if (GRAPH_NAME == 'detect.tflite'):
            GRAPH_NAME = 'edgetpu.tflite'   

    # Get path to current working directory
    CWD_PATH = os.getcwd()

    # Path to video file
    VIDEO_PATH = os.path.join(CWD_PATH,VIDEO_NAME)

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    # Load the Tensorflow Lite model.
    # If using Edge TPU, use special load_delegate argument
    if use_TPU:
        interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        print(PATH_TO_CKPT)
    else:
        interpreter = Interpreter(model_path=PATH_TO_CKPT)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Check output layer name to determine if this model was created with TF2 or TF1,
    # because outputs are ordered differently for TF2 and TF1 models
    outname = output_details[0]['name']

    if ('StatefulPartitionedCall' in outname): # This is a TF2 model
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else: # This is a TF1 model
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    # Open video file
    video = cv2.VideoCapture(VIDEO_PATH)
    imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video.get(cv2.CAP_PROP_FPS)
    


    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # You can choose another codec based on your preferences
    out = cv2.VideoWriter('output_video.avi', fourcc, fps, (int(imW), int(imH)))
    print(tf.__version__)
    classification_model=tf.keras.saving.load_model('C:\\Users\\MSI\\Documents\\GitHub\\InsightTrack-AI-Powered-Demographic-Analysis-and-Counting-for-Public-Spaces-main\\models\\SSD Mobilenet V2\\src\\models\\weights.h5')
    print("Classification Model Loaded ! ")
    tracker=Tracker()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    unique_track_ids=set()

    total_frame=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in tqdm.tqdm(range(total_frame)):

        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = video.read()
        frame_xopy=frame.copy()
        # plt.imshow(frame_xopy)
        # plt.waitforbuttonpress()
        # plt.imshow(frame)
        # plt.waitforbuttonpress()
        start_time=time.time()
        
       
     
        cv2.line(frame,(0,175),(640,175),(0,255,0),2)

        detections=[]
        
        if not ret:
            print('Reached the end of the video!')
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (320, 320))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects
        
        

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                class_id= int(classes[i])
             
               
                detections.append([xmin,ymin,xmax,ymax,scores[i]])
                
                
                
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (255,0,0), 2)#if person, then draw red rectangle
                center_x=int((xmin+xmax)/2)
                center_y=int((ymin+ymax)/2)
                cv2.circle(frame,(int(center_x),int(center_y)),4,(0,255,0),-1) #draw circle to the center
                   
                    # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                
                # cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                # cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text


        """
        Deep Sort 
        """
        
      
            
        
        tracker.update(frame,detections)
            
        for track in tracker.tracks:
                bbox=track.bbox
                p_bbox=list(map(int,track.bbox))
                track_id=track.track_id
                
                x1, y1, x2, y2 = p_bbox
                
                center_x=int((x1+x2)/2)
                center_y=int((y1+y2)/2)
                
                
                
                draw_info(frame,track_id,p_bbox,0)
                
                if track_id not in tracked_people:
                    if center_y >=175:
                        # print([x1,y1,x2,y2])
                        # image=frame_xopy[x1:x2,y1:y2]
                        # image=cv2.resize(image,(224,224))
                        # plt.imshow(image)
                        # plt.waitforbuttonpress()
                        #classification(image,classification_model)
                    #     image_cropped= crop(x1,y1,x2,y2)
                    #     resize(image_cropped,(224,224))
                    #     label=model.predict(image_cropped)
                         
                    #     if label==0:
                    #       man_count+1  
                        cropped_image=frame_xopy[y1:y2,x1:x2]
                        print(cropped_image.shape)
                        # resized_image=cv2.resize(cropped_image,(224,224))
                        
                        result=classification(cropped_image,classification_model)
                        plt.imshow(cropped_image)
                        plt.title(result)
                        plt.waitforbuttonpress()
                        
                        tracked_people[track_id]=True
                        person_count+=1
                
                
     

            
            
        
        end_time = time.time()  # İşlem bitiş zamanını kaydet
        elapsed_time = end_time - start_time  # Geçen süreyi hesapla
        fps = 1 / elapsed_time  # FPS değerini hesapla
        fps = "{:.2f}".format(fps)
        draw_frame_text=return_frame_with_count_info(frame,person_count,fps)
        # All the results have been drawn on the frame, so it's time to display it.
       
        out.write(frame)
   
    # Clean up
    video.release()
    out.release()