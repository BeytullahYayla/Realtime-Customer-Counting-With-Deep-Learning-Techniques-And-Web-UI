import cv2
import numpy as np
import tensorflow as tf


class CustomerClassification:
    
    def __init__(self,model_path:str) -> None:
        
        self.model=tf.keras.saving.load_model('models\\weights.h5')
    
    def __get_label_name(self,index:int):
        LABELS={
            0:"Employee",
            1:"Kid",
            2:"Man",
            3:"Staff",
            4:"Woman"
        }
        return LABELS[index]
    # Test veri setini yükleyip ön işleme yapma fonksiyonu
    def __load_and_preprocess_image(self,img):
        img = cv2.resize(img, (224, 224))
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = img / 255.0  # normalize to [0,1] range
        img_array = np.expand_dims(img, axis=0)
        return img_array
    

    def classification(self,image):
        preprocessed_img=self.__load_and_preprocess_image(image)
        y_pred=self.model.predict(preprocessed_img)
        y_pred=np.argmax(y_pred,axis=1)
        print(y_pred)
        return self.__get_label_name(y_pred[0])
