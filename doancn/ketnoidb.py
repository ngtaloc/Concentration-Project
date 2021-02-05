import cv2
import numpy as np
import pyodbc
import os

def insertUpdate(id, ten):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=(LocalDB)\MSSQLLocalDB;'
                          'Database=test;'
                          'Trusted_Connection=Yes'
                          )
    query = "SELECT * FROM THONGTIN WHERE id =" +str(id)
    cursor = conn.execute(query)

    isRecordExits = 0

    for row in cursor:
        isRecordExits = 1
    if(isRecordExits == 0):
        query = "INSERT INTO THONGTIN VALUES("+str(id)+",'"+str(ten) + "')"
    else:
        query ="UPDATE THONGTIN SET ten='"+str(ten)+"' WHERE id="+str(id)
    conn.execute(query)
    conn.commit()
    conn.close()
# load tv

import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

# chen data
id = input("nhap id ")
name = input("nhap ten ")
insertUpdate(id, name)

sampleNum = 0

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 225), 2)
        if( not os.path.exists('dataSet' )):
            os.makedirs('dataSet')
        sampleNum += 1

        cv2.imwrite('dataSet/User.' + str(id)+'.' + str(sampleNum) + '.jpg', gray[y: y + h, x: x + w])
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if sampleNum > 100:
        break
cap.release()
cv2.destroyAllWindows()