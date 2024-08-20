import os
import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt

# # Paths
# path_to_data = "./images/"
# path_to_cr_data = "./images/cropped/"

# # Create directories if they don't exist
# if not os.path.exists(path_to_cr_data):
#     os.mkdir(path_to_cr_data)

# # Cascade classifiers
# face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

# def get_cropped_image_if_2_eyes(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"Image not read correctly: {image_path}")
#         return None
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x,y,w,h) in faces:
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = img[y:y+h, x:x+w]
#         eyes = eye_cascade.detectMultiScale(roi_gray)
#         if len(eyes) >= 2:
#             return roi_color
#     return None

# # List of image directories
# img_dirs = [entry.path for entry in os.scandir(path_to_data) if entry.is_dir()]

# # Dictionary to store cropped images
# celebrity_file_names_dict = {}

# for img_dir in img_dirs:
#     count = 1
#     celebrity_name = os.path.basename(img_dir)
#     celebrity_file_names_dict[celebrity_name] = []
    
#     for entry in os.scandir(img_dir):
#         if entry.is_file():
#             roi_color = get_cropped_image_if_2_eyes(entry.path)
#             if roi_color is not None:
#                 cropped_folder = os.path.join(path_to_cr_data, celebrity_name)
#                 if not os.path.exists(cropped_folder):
#                     os.makedirs(cropped_folder)
                
#                 cropped_file_name = f"{celebrity_name}{count}.png"
#                 cropped_file_path = os.path.join(cropped_folder, cropped_file_name)
                
#                 cv2.imwrite(cropped_file_path, roi_color)
#                 celebrity_file_names_dict[celebrity_name].append(cropped_file_path)
#                 count += 1
#             else:
#                 print(f"No face/eyes detected in: {entry.path}")



def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H

cropped_img = cv2.imread('test.jpg')
im_har = w2d(cropped_img,'db1',5)
plt.imshow(im_har, cmap='gray')