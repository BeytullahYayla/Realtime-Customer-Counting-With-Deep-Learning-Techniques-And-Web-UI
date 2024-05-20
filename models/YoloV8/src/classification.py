import cv2
import numpy as np

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
    return get_label_name(y_pred[0])
