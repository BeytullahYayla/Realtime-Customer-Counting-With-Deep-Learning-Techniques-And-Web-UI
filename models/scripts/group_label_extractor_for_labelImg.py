import cv2
from ultralytics import YOLO
import os
import time
import argparse
from tqdm import tqdm


def parse_arguments():
    argparser=argparse.ArgumentParser()
    argparser.add_argument("--directory",type=str)
    argparser.add_argument("--directory_label",type=str)
    argparser.add_argument("--modeldir",type=str)
    return argparser.parse_args()
    

def write_yolo_format(file, class_id, x, y, width, height):
    file.write(f"{class_id} {x} {y} {width} {height}\n")
    

def predict_from_one_image(frame,model,file_path):
    results=model.predict(frame)
    height, width = frame.shape[:2]
    # Iterate over the results
    for result in results:
        boxes = result.boxes.numpy()  # Get boxes on CPU in numpy format
        for box in boxes:  # Iterate over boxes
                    r = box.xyxy[0].astype(int)  # Get corner points as int
                    class_id = int(box.cls[0])  # Get class ID
                    if class_id == 0:
                        class_id_convert = 1
                
                        normalized_x = ((r[0]+r[2])/2) / width
                        normalized_y = ((r[1] +r[3]) / 2) / height
                        normalized_width = (r[2] - r[0]) / width
                        normalized_height = (r[3] - r[1]) / height
                        
                        print(f"{class_id_convert} {normalized_x} {normalized_y} {normalized_width} {normalized_height}\n")
                        
                        str_to_write=f"{class_id_convert} {normalized_x} {normalized_y} {normalized_width} {normalized_height}\n"
                        return str_to_write
                 
                        
                     
    
def list_files_in_directory(directory,image:True):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if image:
                
                file_path = os.path.join(root, file)
                if file_path.split(".")[-1]=="png":
                    file_list.append(file_path)
            if image==False:
                file_path = os.path.join(root, file)
                if file_path.split(".")[-1]=="txt":
                    file_list.append(file_path)
                
    return file_list

if __name__ == "__main__":
    
    args=parse_arguments()

    directory = args.directory
    directory_label = args.directory_label

    # Load the model
    model = YOLO(args.modeldir,"v8")
    
    # videoların yollarını alıyoruz.
    file_list = list_files_in_directory(directory,image=True)
    file_list_labels = list_files_in_directory(directory_label,image=False)
    
    #print(f"file_list_labels:{file_list_labels}")#list of labels
    
    for file_path, file_list_labels in tqdm(zip(file_list, file_list_labels), total=len(file_list)):
        
        frame=cv2.imread(file_path)
        
        str_to_write=predict_from_one_image(frame,model,file_path)
        
        if str_to_write is not None:
            
            with open(file_list_labels,"a") as file:
                file.write(str_to_write)
        
        
        

