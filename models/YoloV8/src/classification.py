import cv2
import numpy as np
import tensorflow as tf


class CustomerClassification:
    
    def __init__(self,model_path:str) -> None:
        
        self.model=tf.keras.saving.load_model(model_path)
    
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
        img_array=img_array.astype(np.float32)
        return img_array
    

    def classification(self,image):
        preprocessed_img=self.__load_and_preprocess_image(image)
        y_pred=self.model.predict(preprocessed_img)
        y_pred=np.argmax(y_pred,axis=1)
        print(y_pred)
        return self.__get_label_name(y_pred[0])
    def classification_tflite(self,image):
        # Load the TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path="models\\mobilenet_v2_1.0_224.tflite")
        interpreter.allocate_tensors()
    
        input_data=self.__load_and_preprocess_image(image)
        result=self.__classify_image(interpreter,input_data)
        result=self.__get_label_name(int(result))
        return result
      
        
    def __set_input_tensor(self,interpreter, input):
            input_details = interpreter.get_input_details()[0]
            print(input_details)
            tensor_index = input_details['index']
            input_tensor = interpreter.tensor(tensor_index)()[0]
            # Inputs for the TFLite model must be uint8, so we quantize our input data.
            # NOTE: This step is necessary only because we're receiving input data from
            # ImageDataGenerator, which rescaled all image data to float [0,1]. When using
            # bitmap inputs, they're already uint8 [0,255] so this can be replaced with:
            #   input_tensor[:, :] = input
            # scale, zero_point = input_details['quantization']
            # input_tensor[:, :] = np.float32(input / scale + zero_point)
            
    def __classify_image(self,interpreter, input):
            self.__set_input_tensor(interpreter, input)
            interpreter.invoke()
            output_details = interpreter.get_output_details()[0]
            output = interpreter.get_tensor(output_details['index'])
                # Outputs from the TFLite model are uint8, so we dequantize the results:
            # scale, zero_point = output_details['quantization']
            # output = scale * (output - zero_point)
            top_1 = np.argmax(output)
            return top_1
                
                
            
        
        
