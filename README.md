# Real-Time Customer Counting Using Deep Learning Techniques

## 🚩 Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
  * [Customer Detection](#customer-detection)
  * [Customer Counting Algorithm](#customer-counting-algorithm)
  * [Customer Classification](#customer-classification)
  * [Customer Tracking](#customer-tracking)
  * [User-Interactive Interface](#user-interactive-interface)
- [Flowcharts](#flowcharts)
- [Contact Information](#contact-information)

## Project Overview

This project focuses on utilizing images captured by in-store security cameras to perform various analyses. The application offers store managers essential functions such as customer detection, classification based on demographic characteristics, and customer counting. The customer detection function determines the number of people entering and exiting the store, while the classification feature groups customers by age, gender, and other demographics. The counting function monitors customer density in the store at specific time intervals. All these data are presented to store managers via a user-friendly web interface, enabling a detailed analysis of store performance and customer behavior. This allows managers to make more informed and data-driven operational decisions. Our application uses modern computer vision and machine learning techniques to provide real-time and historical data analyses, thereby enhancing store management efficiency and effectiveness.

## Technologies Used

- **Programming Languages**: Python, JavaScript
- **Frameworks**: FastAPI, React
- **Database**: MySQL
- **Containerization**: Docker
- **Deep Learning Libraries**: Keras, OpenCV, Pytorch
- **Object Detection Algorithms**: YOLOv8, DeepSort

## Features

### Customer Detection
Using deep learning and computer vision techniques, customer detection is implemented with the YOLOv8 algorithm. YOLOv8 is an algorithm that uses a convolutional neural network (CNN) to detect objects in real-time, offering high accuracy and speed. Approximately 90,000 training data were used for object detection in the project.

![image](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/3e70be26-ab7c-4969-8735-3be43e52aac2)

![person-detection-retail-0013](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/8820ac34-efae-4351-a2b3-762a76dc828b)


### Customer Counting Algorithm
The customer counting algorithm aims to determine the number of customers in the store in real-time using deep learning and computer vision techniques. In this project, YOLOv8 and DeepSort algorithms were used together. Initially, the YOLOv8 algorithm detects individuals in the store. Then, the DeepSort algorithm tracks the detected individuals and assigns a unique identity to each person. This way, the number of people entering and exiting the store is determined and recorded based on the movements of the detected and tracked individuals. This method provides necessary data to store managers by monitoring customer density and movements in the store.

![Customer_Counting](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/51371a0b-a60b-4d9f-aee1-f929a9e79d3b)



### Customer Classification
Customer classification is performed using deep learning and image processing techniques. In this project, a customer classification model was developed using the MobileNetV2 architecture. MobileNetV2 is a lightweight and efficient CNN architecture designed for image applications, especially on mobile and embedded devices. The training process was conducted on Google Colab, using approximately 130,000 images to enhance model accuracy. Transfer learning and fine-tuning techniques were used to optimize the model's performance.

![Screenshot_1](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/5edfe4bb-4eb9-4e83-85e8-c5da67b2b95c)


### Customer Tracking
Human tracking is performed using the DeepSort (Simple Online Realtime Tracking) algorithm in this project. DeepSort is an algorithm that uses Kalman filtering and deep learning-based feature extraction to track objects in real-time. This is one of the crucial steps to ensure the proper functioning of the subsequent counting algorithm.

![image](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/a6ee647c-d053-4a73-bcab-9bf32df075d2)

![person-detection-retail-0013](https://github.com/BeytullahYayla/Insight-Track-AI-Powered-Demographic-Analysis/assets/78471151/1b348315-4a42-4c31-aed7-7d9e11b70f4e)


### User-Interactive Interface
The project's frontend was developed using ReactJS to provide a user-friendly web interface. The web interface visualizes in-store customer data and provides managers with the necessary information to make strategic decisions. Communication with the backend is facilitated via API, providing real-time data flow to the user. This allows store managers to easily monitor customer traffic, demographic information, and other vital data.

## Flowcharts

- Customer Counting Algorithm Flowchart
- YOLOv8 Architecture
- Customer Classification Model Architecture

## Contact Information

**Advisor:** Prof. Dr. Nejat Yumuşak  
**Department of Computer Engineering, Sakarya University**

**Contributors:**
- Beytullah Yayla  
  Email: beytullahyayla1@gmail.com
  
- Mehmet Ataş  
  Email: mehmet.atas5@gmail.com

- Mehmet Oğuz Özkan  
  Email: mehmet.ozkan5@ogr.sakarya.edu.tr
