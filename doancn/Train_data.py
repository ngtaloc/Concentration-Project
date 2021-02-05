from tkinter import Image

import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

# lay duong dan anh
def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
 #   print(imagePaths) #in duong dan anh
    faces = []
    IDs = []
# chuyen doi anh thanh ma tran
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')  #lay du lieu anh
        print(faceNp)   #in anh ve dang array
        get_Id = int(imagePath.split('.')[1])  #lay du lieu ID
        print ("\ngetid=",get_Id)
        faces.append(faceNp)
        IDs.append(get_Id)
        cv2.imshow('trainning', faceNp)
        cv2.waitKey(10)
    return faces, IDs

faces , Ids = getImageWithID(path)
recognizer.train(faces, np.array(Ids))    #train
# tao file recognizer
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
recognizer.save('recognizer/trainningData.yml')

cv2.destroyAllWindows()

