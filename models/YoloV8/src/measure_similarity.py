# import cv2
# import numpy as np

# def mse(imageA, imageB):
#     # MSE hesaplama
#     err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
#     err /= float(imageA.shape[0] * imageA.shape[1])
#     return err

# # İki resmi yükleme
# img1 = cv2.imread('cropped\\out_cropped11.png')
# img2 = cv2.imread('cropped\\out_cropped11.png')

# #Resize
# img1=cv2.resize(img1,(224,224))
# img2=cv2.resize(img2,(224,224))

# # Resimleri gri tonlamaya dönüştürme
# img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# # MSE hesaplama
# mse_value = mse(img1_gray, img2_gray)
# print(f"MSE: {mse_value}")

import cv2
import os
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp

# İki resmi yükleme
img1 = cv2.imread('cropped\\out_cropped3.png')
img1=cv2.resize(img1,(224,224))
for image_path in os.listdir('cropped'):
    
    img2 = cv2.imread("cropped\\"+image_path)
    img2=cv2.resize(img2,(224,224))
    #Resize

    print("MSE: ", mse(img1,img2))
    print("RMSE: ", rmse(img1, img2))
    print("PSNR: ", psnr(img1, img2))
    print("SSIM: ", ssim(img1, img2))
    print("UQI: ", uqi(img1, img2))
    print("MSSSIM: ", msssim(img1, img2))
    print("ERGAS: ", ergas(img1, img2))
    print("SCC: ", scc(img1, img2))
    print("RASE: ", rase(img1, img2))
    print("SAM: ", sam(img1, img2))
    print("VIF: ", vifp(img1, img2))
    print("--------------------------------------")
    print()
