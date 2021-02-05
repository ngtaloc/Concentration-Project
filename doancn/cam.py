from datetime import time

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
"""cap = cv2.VideoCapture(0)

while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('DETECTING FACE', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
cap.release()
cv2.destroyALLWindows()
"""
  # Will hold the image address location
tmp = None  # Will hold the temporary image for display
brightness_value_now = 0  # Updated brightness value
blur_value_now = 0  # Updated blur value
fps = 0
started = False

def loadcam(btn_D_startcam, label_D_cam):
    global started
    if started:
        started = False
        btn_D_startcam.setText('Bắt đầu điểm danh')
    else:
        started = True
        btn_D_startcam.setText('Kết thúc điểm danh')

    vid = cv2.VideoCapture(0)

    print(vid.isOpened())
    while (vid.isOpened()):
        img, frame = vid.read()
        frame = imutils.resize(frame, height=600, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.12,
            minNeighbors=5,
            minSize=(30, 30)
            # flags=cv2.CV_HAAR_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 228, 220), 2)
        print('this')
        displayImage(label_D_cam, frame, 1)

        key = cv2.waitKey(1) & 0xFF
        if self.started == False:
            break
            print('Loop break')


def displayImage(label_D_cam, img, window=1):
    qformat = QImage.Format_Indexed8

    if len(img.shape) == 3:
        if (img.shape[2]) == 4:
            qformat = QImage.Format_RGBA888
        else:
            qformat = QImage.Format_RGB888
    img = QImage(img, img.shape[1], img.shape[0], qformat)
    imf = img.rgbSwapped()
    label_D_cam.setPixmap(QPixmap.fromImage(img))
    label_D_cam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def loadcam1():
        vid = cv2.VideoCapture(0)
        print(vid.isOpened())
        while (vid.isOpened()):
            img, frame = vid.read()
            #frame = imutils.resize(frame, height=600, width=800)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.12,
                minNeighbors=5,
                minSize=(30, 30)
                #flags=cv2.CV_HAAR_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 228, 220), 2)
                cv2.line(frame, (int((x+x+w)/2), y), (int((x+x+w)/2), y + h), (10, 228, 220), 2)
                cv2.line(frame, (x, int((y+y+h) /2)),(x + w, int((y+y+h) /2)) , (10, 228, 220), 2)


            #self.displayImage1(frame, 1)
            cv2.imshow('', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == "q":
                break
                print('Loop break')
        vid.release()
        cv2.destroyAllWindows()
def displayImage1(self, img,window=1):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0],qformat)
        imf = img.rgbSwapped()
        self.label_D_cam.setPixmap(QPixmap.fromImage(img))
        self.label_D_cam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

loadcam1()