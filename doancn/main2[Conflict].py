import os
import sys
from datetime import datetime
from PIL import Image

import cv2, imutils
import numpy as np
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *

import QLSinhVien
import DataConn
from Controllers import XLDL

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer = cv2.face.createLBPHFaceRecognizer()

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == '' and
            self.textPass.text() == ''):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

class maincode(QMainWindow):
    def __init__(self):
        super(maincode, self).__init__()
        uic.loadUi("diemdanh2.ui", self)

        # Tab điểm danh
        self.started = False
        self.btnTScam = False
        self.btnquet = False #biến kiểm tra button có clink hay k
        self.btn_D_sCam = self.findChild(QPushButton, "btn_D_startcam")
        self.label_D_cam = self.findChild(QLabel, "label_D_cam")
        self.cbb_D_Lophoc = self.findChild(QComboBox, "cbb_D_Lophoc")
        self.DT_D_NgayDD = self.findChild(QDateTimeEdit, "dte_D_ngayDD")
        self.TW_D_dsSV = self.findChild(QTableView, "TW_D_dsSV")

        self.btn_D_sCam.clicked.connect(self.click_btn_startcam)
        self.cbb_D_Lophoc.currentIndexChanged.connect(self.loadSV)
        self.DT_D_NgayDD.setDateTime(datetime.now())


        # Tab Thêm SV
        self.btn_T_sCam = self.findChild(QPushButton, "btn_T_KDcam")
        self.btn_T_quet = self.findChild(QPushButton, "btn_T_Quet")
        self.btn_T_luu = self.findChild(QPushButton, "btn_T_luu")
        self.btn_T_Xoa = self.findChild(QPushButton, "btn_T_xoa")
        self.label_T_cam = self.findChild(QLabel, "label_T_cam")
        self.label_T_hinh = self.findChild(QLabel, "label_T_hinh")
        self.txt_T_tensv = self.findChild(QLineEdit, "txt_T_tensv")
        self.txt_T_masv = self.findChild(QLineEdit, "txt_T_masv")
        self.cbb_T_lop = self.findChild(QComboBox, "cbb_T_lop")
        self.txt_T_DiaChi = self.findChild(QLineEdit, "txt_T_DiaChi")
        self.rdo_T_nam = self.findChild(QRadioButton, "rdo_T_nam")
        self.rdo_T_nu = self.findChild(QRadioButton, "rdo_T_nu")

        self.btn_T_luu.clicked.connect(self.clink_btn_TLuu)
        self.btn_T_Xoa.clicked.connect(self.click_btn_Txoa)
        self.btn_T_sCam.clicked.connect(self.click_btn_startcamT)
        self.btn_T_quet.clicked.connect(self.click_btn_Quet)
        # Tab Lớp

        # Tab Môn học
        self.txt_L_malop = self.findChild(QLineEdit, "txt_L_malop")
        self.txt_L_tenlop = self.findChild(QLineEdit, "txt_L_tenlop")
        self.btn_L_sua = self.findChild(QPushButton, "btn_L_sua")
        self.btn_L_xoa = self.findChild(QPushButton, "btn_L_xoa")
        self.btn_L_them = self.findChild(QPushButton, "btn_L_them")


#TAB Lớp học ( Quản lý SV)
        self.txt_LH_timSV = self.findChild(QLineEdit, "txt_LH_timSV")
        self.btn_LH_tim = self.findChild(QPushButton, "btn_LH_tim")
        self.btn_LH_Them = self.findChild(QPushButton, "btn_LH_Them")
        self.btn_LH_themALL = self.findChild(QPushButton, "btn_LH_themALL")
        self.btn_LH_bo = self.findChild(QPushButton, "btn_LH_bo")
        self.btn_LH_BoALL = self.findChild(QPushButton, "btn_LH_BoALL")
        self.cbb_LH_lop = self.findChild(QComboBox, "cbb_LH_lop")
        self.cbb_LH_lophoc = self.findChild(QComboBox, "cbb_LH_lophoc")
        self.tw_LH_DSLopHoc = self.findChild(QTableView, "tw_LH_DSLopHoc")
        self.tw_LH_DSsv = self.findChild(QTableView, "tw_LH_DSsv")


        self.cbb_LH_lophoc.currentIndexChanged.connect(self.load_tw_LH_DSLopHoc)
        self.cbb_LH_lop.currentIndexChanged.connect(self.load_tw_LH_DSsv)
        self.btn_LH_tim.clicked.connect(self.clink_btn_LH_tim)

        self.btn_LH_Them.clicked.connect(self.clink_btn_LH_Them)
        self.btn_LH_themALL.clicked.connect(self.clink_btn_LH_themALL)
        self.btn_LH_bo.clicked.connect(self.clink_btn_LH_bo)
        self.btn_LH_BoALL.clicked.connect(self.clink_btn_LH_BoALL)

        self.load()
        self.show()


#TAB Quản lý SV (Lớp học)
    def load_tw_LH_DSLopHoc(self): #load dssv theo lớp học (CS434A)
        QLSinhVien.loadDSSV_LopHoc(self.tw_LH_DSLopHoc, self.cbb_LH_lophoc.currentText())

    def load_tw_LH_DSsv(self): # load dssv theo lớp sinh hoạt (TMP2)
        QLSinhVien.loadDSSV_Lop(self.tw_LH_DSsv, self.cbb_LH_lop.currentText())

    def clink_btn_LH_tim(self):# click btn tìm
        QLSinhVien.click_btn_tim(self.tw_LH_DSsv, self.txt_LH_timSV.text())

    def clink_btn_LH_Them(self):
        dssv =  self.tw_LH_DSsv
        QLSinhVien.them(self.tw_LH_DSLopHoc)

    def clink_btn_LH_themALL(self):
        QLSinhVien.themALL(self.tw_LH_DSLopHoc)

    def clink_btn_LH_bo(self):
        QLSinhVien.bo(self.tw_LH_DSLopHoc)

    def clink_btn_LH_BoALL(self):
        QLSinhVien.boALL(self.tw_LH_DSLopHoc, self.txt_LH_timSV.text())


# pageLOAD
    def load(self):
        # load CBB danh sách lớp TAB THÊM
        dsLop = XLDL.xldl_lop.layDSLop()
        for i in dsLop:
            self.cbb_T_lop.addItem(i.getMalop())
            self.cbb_LH_lop.addItem(i.getMalop())

        # load CBB Lớp học TAB DD
        dsLophoc = XLDL.xldl_LopHoc.layDSLopHoc()
        for i in dsLophoc:
            self.cbb_D_Lophoc.addItem(i.getTenLH())
            self.cbb_LH_lophoc.addItem(i.getTenLH())

        # load danh sách sinh viên


    #load sinh viên theo CBB
    def loadSV(self):
        # load danh sách sinh viên
        malophoc = self.cbb_D_Lophoc.currentText()
        ngaydd = self.DT_D_NgayDD.dateTime().toString(self.DT_D_NgayDD.displayFormat())
        ngaydd = ngaydd.split(' ')[0]

        dsSinhVien = XLDL.xldl_SinhVien.layDSsinhVien(malophoc[:6],ngaydd)
        row = 0
        self.TW_D_dsSV.setRowCount(len(dsSinhVien))
        for sv in dsSinhVien:
            self.TW_D_dsSV.setItem(row, 0, QTableWidgetItem(sv.getmaSV()))
            self.TW_D_dsSV.setItem(row, 1, QTableWidgetItem(sv.getTenSV()))
            self.TW_D_dsSV.setItem(row, 2, QTableWidgetItem(sv.getgioitinh()))
            self.TW_D_dsSV.setItem(row, 3, QTableWidgetItem(sv.getdiachi()))
            self.TW_D_dsSV.setItem(row, 4, QTableWidgetItem(sv.getVang()))
            row = row +1

#TAB ĐIỂM DANH

    #lấy thông tin sv
    def getprofile(self, id):
        conn = DataConn.DBConnet.getConnet()
        query = "SELECT * FROM Sinhvien where masv ='sv" + str(id)+"'"
        print(query)
        cursor = conn.execute(query)

        profile = None
        for row in cursor:
            profile = row
        conn.close()
        return profile

    # Star cam
    def click_btn_startcam(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(r'recognizer\trainningData.yml')
        if self.started:
            self.started = False
            self.btn_D_sCam.setText('Bắt đầu điểm danh')
        else:
            self.started = True
            self.btn_D_sCam.setText('Kết thúc điểm danh')

        vid = cv2.VideoCapture(0)

        fontface = cv2.FONT_HERSHEY_SIMPLEX
        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, height=600, width=800)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
                # flags=cv2.CV_HAAR_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 228, 220), 2)
                roi_gray = gray[y:y + h, x:x + w]
                id, confidence = recognizer.predict(roi_gray)

                if confidence < 45:
                    profile = self.getprofile(id)
                    if (profile != None):
                        cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                        print('pro= ', profile)
                        malophoc = self.cbb_D_Lophoc.currentText()
                        ngaydd = self.DT_D_NgayDD.dateTime().toString(self.DT_D_NgayDD.displayFormat())
                        ngaydd = ngaydd.split(' ')[0]


                        conn = DataConn.DBConnet.getConnet()
                        query = "SELECT * FROM Diemdanh WHERE malophoc='" + malophoc[:6] + "' and masv='"+profile[0]+"' and ngaydd='"+ngaydd+"'"
                        cursor = conn.execute(query)

                        isRecordExits = 0

                        for row in cursor:
                            isRecordExits = 1
                        if (isRecordExits == 0):
                            query = "insert into Diemdanh values ('"+malophoc[:6]+"', '"+profile[0]+"', '"+ngaydd+"', 'True' )"
                            print('them')
                            print(query)

                        conn.execute(query)
                        conn.commit()
                        conn.close()

                        """qery = "insert into Diemdanh values ('"+malophoc[:6]+"', '"+profile[0]+"', '"+ngaydd+"', 'True' )"

                        try:
                            conn = DataConn.DBConnet.getConnet()
                            conn.execute(qery)
                            conn.commit()
                            conn.close()
                            print('dd thành công')
                            qery1=qery
                        except:
                            #QMessageBox.about(self, "Thông báo", "Sinh viên đã điểm danh rồi")
                            print('diem danh roi')
                            break"""

                        self.loadSV()

                else:
                    cv2.putText(
                        frame, "NO", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
            self.displayImageLAYBEL(frame, self.label_D_cam, 1)

            key = cv2.waitKey(1) & 0xFF
            if self.started == False:
                vid.release()
                self.label_D_cam.setText('Bật camera để tiếp tục')
                #break
                print('Loop break')

#TAB THÊM SINH VIÊN

    # btn xoa
    def click_btn_Txoa(self):
        if self.txt_T_masv.text() != '':
            #confirm btn xóa
            buttonReply = QMessageBox.question(self, 'Xác nhân xóa', "Bạn có chắc chắn xóa sinh viên này?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes :
                #kết nối database
                conn = DataConn.DBConnet.getConnet()
                query = "Delete FROM SinhVien WHERE masv='" + self.txt_T_masv.text() + "'"
                try:
                #xóa trong data
                    conn.execute(query)

                #xóa hình của sv
                    imagePaths = [os.path.join('dataSet', f) for f in os.listdir('dataSet') if f.split('.')[1]==self.txt_T_masv.text().split('sv')[1]]
                    #imagePaths là đường dẫn ảnh

                    for imagePath in imagePaths: # thực hiện xóa ảnh face
                        print(imagePath)
                        os.remove(imagePath)
                    QMessageBox.about(self, "Thông báo", "Xóa thành công!")
                except Exception as e:
                    print(e)
                    QMessageBox.about(self, "ERRO!", e)
                conn.commit()
                conn.close()
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền mã sinh viên để xóa!")


    # Them btn luu
    def clink_btn_TLuu(self):
        if self.txt_T_masv.text() != '' and self.txt_T_tensv.text() !='' and self.txt_T_DiaChi.text() != '' and self.cbb_T_lop.currentText() != '' and (self.rdo_T_nam.isChecked() or self.rdo_T_nu.isChecked()):
            #confirm btn lưu
            buttonReply = QMessageBox.question(self, 'Xác nhân sửa', "Thông tin sinh viên này sẽ được cập nhật!",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                #kết nối database
                conn = DataConn.DBConnet.getConnet()
                gt = 'Nam'
                if self.rdo_T_nu.isChecked():
                    gt = 'Nữ'
                query = "UPDATE SinhVien SET tensv=N'" + self.txt_T_tensv.text() + "' , malop='" + self.cbb_T_lop.currentText() + "', diachi=N'" + self.txt_T_DiaChi.text() + "', gioitinh=N'" + gt + "' WHERE masv= '" + self.txt_T_masv.text() + "'"
                try:
                    conn.execute(query)
                    QMessageBox.about(self, "Thông báo", "Lưu thành công!")
                except Exception as e:
                    print(e)
                    QMessageBox.about(self, "ERRO!", e)
                conn.commit()
                conn.close()
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền đầy đủ thông tin sinh viên!")

    #clibk Quét để thay đổi data
    def click_btn_Quet(self):
        if self.btnTScam == True:
            if self.txt_T_masv.text() != None and self.txt_T_tensv.text() !=None and self.txt_T_DiaChi.text() != None and self.cbb_T_lop.currentText() != None and (self.rdo_T_nam.isChecked() or self.rdo_T_nu.isChecked()):
                if self.btnquet:
                    self.btnquet = False
                    self.btn_T_quet.setText('Bắt đầu quét')
                else:
                    self.btnquet = True
                    self.btn_T_quet.setText('Kết thúc quét')
            else:
                QMessageBox.about(self, "Thông báo", "Vui lòng điền thông tin sinh viên vào")

            if self.btnquet:
                conn = DataConn.DBConnet.getConnet()
                gt = 'Nam'
                if self.rdo_T_nu.isChecked():
                    gt = 'Nữ'
                """try:
                    query = "INSERT INTO SinhVien VALUES(" + self.txt_T_masv.text() + ", N'" + self.txt_T_tensv.text() + "','" + self.cbb_T_lop.currentText() + "', N'" + self.txt_T_DiaChi.text() + "', N'" + gt + "')"
                    conn.execute(query)
                    print('them')
                except:
                    query = "UPDATE SinhVien SET tensv=N'" + self.txt_T_tensv.text() + "' , malop='" + self.cbb_T_lop.currentText()+ "', diachi=N'" + self.txt_T_DiaChi.text() + "', gioitinh=N'" + gt + "' WHERE masv= '"+self.txt_T_masv.text()+"'"
                    conn.execute(query)
                    print('up')"""
                query = "SELECT * FROM SinhVien WHERE masv='"+self.txt_T_masv.text()+"'"
                cursor = conn.execute(query)

                isRecordExits = 0

                for row in cursor:
                    isRecordExits = 1
                if (isRecordExits == 0):
                    query = "INSERT INTO SinhVien VALUES('" + self.txt_T_masv.text() + "', N'" + self.txt_T_tensv.text() + "','" + self.cbb_T_lop.currentText() + "', N'" + self.txt_T_DiaChi.text() + "', N'" + gt + "')"
                    print('them')
                    print(query)
                else:
                    query = "UPDATE SinhVien SET tensv=N'" + self.txt_T_tensv.text() + "' , malop='" + self.cbb_T_lop.currentText()+ "', diachi=N'" + self.txt_T_DiaChi.text() + "', gioitinh=N'" + gt + "' WHERE masv= '"+self.txt_T_masv.text()+"'"
                    print('up')
                conn.execute(query)
                conn.commit()
                conn.close()
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng khởi đọng camera")

    # Star cam Tab them | Chụp mặt và Học ở đây
    def click_btn_startcamT(self):

        if self.btnTScam:
            self.btnTScam = False
            self.btn_T_sCam.setText('Khởi Động Camera')
        else:
            self.btnTScam = True
            self.btn_T_sCam.setText('Tắt Camera')
            self.btnquet = False
            self.btn_T_quet.setText('Bắt đầu quét')

        vid = cv2.VideoCapture(0)

        sampleNum = 0
        while (vid.isOpened()):
            img, frame = vid.read()
            #frame = imutils.resize(frame, height=600, width=800)
            #frame = imutils.resize(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
                # flags=cv2.CV_HAAR_SCALE_IMAGE
            )
            #if False
            if self.btnquet == True:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 225), 2)
                #tạo forder dataset
                    if (not os.path.exists('dataSet')):
                        os.makedirs('dataSet')
                    sampleNum += 1
                #lưu hình vào forder dataset
                    cv2.imwrite('dataSet/sv.' + str(self.txt_T_masv.text()).split('sv')[1] + '.' + str(sampleNum) + '.jpg', gray[y: y + h, x: x + w])
                #đưa ảnh đã chụp lên laybel hình ở tab thêm
                    #self.displayImageLAYBEL(gray[y: y + h, x: x + w], self.label_T_hinh, 1)
                    self.label_T_hinh.setPixmap(QPixmap('dataSet/sv.' + str(self.txt_T_masv.text()).split('sv')[1] + '.' + str(sampleNum) + '.jpg'))
                #chụp 100 hình
                if sampleNum > 200:

                    faces, Ids = self.getImageWithID(self.txt_T_masv.text())    # lây mặt và masv của sv
                    if os.path.exists("recognizer/trainningData.yml"):
                        recognizer.read("recognizer/trainningData.yml") # đọc file train
                        print('loadtrain')
                    recognizer.update(faces, np.array(Ids))  # update mặt và masv lên file train
                    if not os.path.exists('recognizer'):    # tao file recognizer
                        os.makedirs('recognizer')
                    recognizer.save('recognizer/trainningData.yml')#lưu file train

                    imagePaths = [os.path.join('dataSet', f) for f in os.listdir('dataSet') if
                                  f.split('.')[1] == self.txt_T_masv.text().split('sv')[1]]
                    for imagePath in imagePaths: # xóa ảnh face đã học
                        print('xóa xong ', imagePath)
                        os.remove(imagePath)

                    QMessageBox.about(self, "Thông báo", "Đã quét xong")
                    cv2.destroyAllWindows()
                    self.btnTScam = True
                    self.btn_T_sCam.setText('Tắt Camera')
                    self.btnquet = False
                    self.btn_T_quet.setText('Bắt đầu quét')

            self.displayImageLAYBEL(frame, self.label_T_cam , 1) # show cam lên laybel

            key = cv2.waitKey(1) & 0xFF
            if self.btnTScam == False:
                vid.release()
                self.label_T_cam.setText('Bật camera để tiếp tục')
                self.btnquet = False
                self.btn_T_quet.setText('Bắt đầu quét')
                #break
                print('Loop break')

    # lấy ảnh Face đã mã hóa và masv
    def getImageWithID(self, masv):
        imagePaths = [os.path.join('dataSet', f) for f in os.listdir('dataSet') if f.split('.')[1] == masv.split('sv')[1]]
        #   print(imagePaths) #in duong dan anh
        faces = []
        IDs = []
        # chuyen doi anh thanh ma tran
        for imagePath in imagePaths:

            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')  # lay du lieu anh
            print(faceNp)  # in anh ve dang array
            get_Id = int(imagePath.split('.')[1])  # lay du lieu ID
            print ("\ngetid=",get_Id)
            faces.append(faceNp)
            IDs.append(get_Id)
            #cv2.imshow('trainning', faceNp)
            #cv2.waitKey(10)
        return faces, IDs

    # load cam len label
    def displayImageLAYBEL(self, img, laybel, window=1):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        laybel.setPixmap(QPixmap.fromImage(img))
        laybel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)



if __name__ == "__main__":
    """app = QApplication(sys.argv)
    window = maincode()
    # window.show()
    app.exec_()"""

    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = maincode()
        window.show()
        sys.exit(app.exec_())
