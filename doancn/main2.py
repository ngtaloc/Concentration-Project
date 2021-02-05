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

import QLLopHoc
import QLMonHoc
import QLLopsinhhoat
import QLSinhVien
import DataConn
import QLThongKe
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
        self.cbb_D_NamHoc = self.findChild(QComboBox, "cbb_D_NamHoc")
        self.cbb_D_Lophoc = self.findChild(QComboBox, "cbb_D_Lophoc")
        self.DT_D_NgayDD = self.findChild(QDateTimeEdit, "dte_D_ngayDD")
        self.TW_D_dsSV = self.findChild(QTableView, "TW_D_dsSV")
        self.TW_D_dsSV.setSortingEnabled(True)

        self.btn_D_sCam.clicked.connect(self.click_btn_startcam)
        self.cbb_D_NamHoc.currentIndexChanged.connect(self.load_DD_LopHoc)
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

        # Tab Lớp (Lớp sinh hoạt)
        self.txt_L_malop = self.findChild(QLineEdit, "txt_L_malop")
        self.txt_L_tenlop = self.findChild(QLineEdit, "txt_L_tenlop")
        self.btn_L_sua = self.findChild(QPushButton, "btn_L_sua")
        self.btn_L_xoa = self.findChild(QPushButton, "btn_L_xoa")
        self.btn_L_them = self.findChild(QPushButton, "btn_L_them")
        self.TW_L_dsLop = self.findChild(QTableView, "TW_L_dsLop")
        self.TW_L_dsLop.setSortingEnabled(True)
        self.btn_L_them.clicked.connect(self.click_btn_L_them)
        self.btn_L_xoa.clicked.connect(self.click_btn_L_xoa)
        self.btn_L_sua.clicked.connect(self.click_btn_L_sua)
        self.TW_L_dsLop.cellClicked.connect(self.dsLopsinhhoat_clicked)
        self.loadDSLopsinhhoat()

        # Tab Môn học
        self.txt_MH_mamh = self.findChild(QLineEdit, "txt_MH_mamh")
        self.txt_MH_tenmh = self.findChild(QLineEdit, "txt_MH_tenmh")
        self.txt_MH_tinchi = self.findChild(QLineEdit, "txt_MH_tinchi")
        self.btn_MH_sua = self.findChild(QPushButton, "btn_MH_sua")
        self.btn_MH_xoa = self.findChild(QPushButton, "btn_MH_xoa")
        self.btn_MH_them = self.findChild(QPushButton, "btn_MH_them")
        self.TW_MH_dsmh = self.findChild(QTableView, "TW_MH_dsmh")
        self.TW_MH_dsmh.setSortingEnabled(True)

        self.btn_MH_them.clicked.connect(self.click_btn_MH_them)
        self.btn_MH_sua.clicked.connect(self.click_btn_MH_sua)
        self.btn_MH_xoa.clicked.connect(self.click_btn_MH_xoa)
        self.TW_MH_dsmh.cellClicked.connect(self.dsMH_clicked)

        self.loadDSMonHoc()

        #TAB danh sách Lớp học ( Quản lý SV)
        self.txt_LH_timSV = self.findChild(QLineEdit, "txt_LH_timSV")
        self.btn_LH_tim = self.findChild(QPushButton, "btn_LH_tim")
        self.btn_LH_Them = self.findChild(QPushButton, "btn_LH_Them")
        self.btn_LH_themALL = self.findChild(QPushButton, "btn_LH_themALL")
        self.btn_LH_bo = self.findChild(QPushButton, "btn_LH_bo")
        self.btn_LH_BoALL = self.findChild(QPushButton, "btn_LH_BoALL")
        self.cbb_LH_Namhoc = self.findChild(QComboBox, "cbb_LH_Namhoc")
        self.cbb_LH_lop = self.findChild(QComboBox, "cbb_LH_lop")
        self.cbb_LH_lophoc = self.findChild(QComboBox, "cbb_LH_lophoc")
        self.tw_LH_DSLopHoc = self.findChild(QTableView, "tw_LH_DSLopHoc")
        self.tw_LH_DSsv = self.findChild(QTableView, "tw_LH_DSsv")
        self.tw_LH_DSLopHoc.setSortingEnabled(True)
        self.tw_LH_DSsv.setSortingEnabled(True)


        self.cbb_LH_Namhoc.currentIndexChanged.connect(self.load_LH_LopHoc)
        self.cbb_LH_lophoc.currentIndexChanged.connect(self.load_tw_LH_DSLopHoc)
        self.cbb_LH_lop.currentIndexChanged.connect(self.load_tw_LH_DSsv)
        self.btn_LH_tim.clicked.connect(self.clink_btn_LH_tim)

        self.btn_LH_Them.clicked.connect(self.clink_btn_LH_Them)
        self.btn_LH_themALL.clicked.connect(self.clink_btn_LH_themALL)
        self.btn_LH_bo.clicked.connect(self.clink_btn_LH_bo)
        self.btn_LH_BoALL.clicked.connect(self.clink_btn_LH_BoALL)

        self.tw_LH_DSLopHoc.cellClicked.connect(self.dsLH_clicked)
        self.tw_LH_DSsv.cellClicked.connect(self.dsSV_clicked)
        self.dsMasv = [] #danh sách mã sinh viên được chọn
        self.dsMasvLH = [] #danh sách mã sinh viên được chọn

    #TAB Thống kê
        # TAB thống kê Lop Hoc
        self.cbb_TK_LH_NamHoc = self.findChild(QComboBox, "cbb_TK_LH_NamHoc")
        self.cbb_TK_LH_LopHoc = self.findChild(QComboBox, "cbb_TK_LH_LopHoc")
        self.tw_TK_LH = self.findChild(QTableView, "tw_TK_LH")
        self.btn_TK_LH_xuat = self.findChild(QPushButton, "btn_TK_LH_xuat")
        self.btn_TK_LH_bieuDo = self.findChild(QPushButton, "btn_TK_LH_bieuDo")
        self.label_TK_LH_BieuDo = self.findChild(QLabel, "label_TK_LH_BieuDo")
        self.txt_TK_LH_Malop = self.findChild(QLabel, "txt_TK_LH_Malop")
        self.txt_TK_HL_TenLop = self.findChild(QLabel, "txt_TK_HL_TenLop")
        self.txt_TK_LH_GV = self.findChild(QLabel, "txt_TK_LH_GV")
        self.txt_TK_LH_siso = self.findChild(QLabel, "txt_TK_LH_siso")
        self.txt_TK_LH_tongV = self.findChild(QLabel, "txt_TK_LH_tongV")

        self.tw_TK_LH.setSortingEnabled(True)
        self.cbb_TK_LH_NamHoc.currentIndexChanged.connect(self.load_TK_LH_NamHoc)
        self.cbb_TK_LH_LopHoc.currentIndexChanged.connect(self.load_TK_LH_LopHoc)
        self.tw_TK_LH.cellClicked.connect(self.ds_TK_LH_clicked)
        self.btn_TK_LH_xuat.clicked.connect(self.clink_btn_TK_LH_xuat)
        self.btn_TK_LH_bieuDo.clicked.connect(self.clink_btn_TK_LH_bieuDo)
        self.songay=0

        # TAB thống kê SinhVien
        self.cbb_TK_SV_Lop = self.findChild(QComboBox, "cbb_TK_SV_Lop")
        self.cbb_TK_SV_sv = self.findChild(QComboBox, "cbb_TK_SV_sv")
        self.tw_TK_SV = self.findChild(QTableView, "tw_TK_SV")
        self.btn_TK_SV_xuat = self.findChild(QPushButton, "btn_TK_SV_xuat")
        self.btn_TK_HS_bieuDo = self.findChild(QPushButton, "btn_TK_HS_bieuDo")
        self.label_TK_SV_BieuDo = self.findChild(QLabel, "label_TK_SV_BieuDo")
        self.txt_TK_HS_masv = self.findChild(QLabel, "txt_TK_HS_masv")
        self.txt_TK_HS_tenSV = self.findChild(QLabel, "txt_TK_HS_tenSV")
        self.txt_TK_HS_NgaySinh = self.findChild(QLabel, "txt_TK_HS_NgaySinh")
        self.txt_TK_HS_GioiTinh = self.findChild(QLabel, "txt_TK_HS_GioiTinh")
        self.txt_TK_HS_diaChi = self.findChild(QLabel, "txt_TK_HS_diaChi")
        self.txt_TK_HS_TongV = self.findChild(QLabel, "txt_TK_HS_TongV")

        self.tw_TK_SV.setSortingEnabled(True)
        self.cbb_TK_SV_Lop.currentIndexChanged.connect(self.load_TK_SV_CBBsv)
        self.cbb_TK_SV_sv.currentIndexChanged.connect(self.load_TK_SV_TWSV)
        self.tw_TK_SV.cellClicked.connect(self.ds_TK_SV_clicked)
        self.btn_TK_HS_bieuDo.clicked.connect(self.clink_btn_TK_HS_bieuDo)
        self.btn_TK_SV_xuat.clicked.connect(self.clink_btn_TK_SV_xuat)

        # Tab Lớp học
        self.cbb_LopHoc_MaGV = self.findChild(QComboBox, "cbb_LopHoc_MaGV")
        self.cbb_LopHoc_MaMH = self.findChild(QComboBox, "cbb_LopHoc_MaMH")
        self.cbb_LopHoc_Nam = self.findChild(QComboBox, "cbb_LopHoc_Nam")
        self.txt_LopHoc_MaLopHoc = self.findChild(QLineEdit, "txt_LopHoc_MaLopHoc")
        self.txt_LopHoc_TenLopHoc = self.findChild(QLineEdit, "txt_LopHoc_TenLopHoc")
        self.txt_LopHoc_siso = self.findChild(QLineEdit, "txt_LopHoc_siso")
        self.tw_LopHoc_dsLopHoc = self.findChild(QTableView, "tw_LopHoc_dsLopHoc")
        self.btn_LopHoc_Them = self.findChild(QPushButton, "btn_LopHoc_Them")
        self.btn_LopHoc_Sua = self.findChild(QPushButton, "btn_LopHoc_Sua")
        self.btn_LopHoc_Xoa = self.findChild(QPushButton, "btn_LopHoc_Xoa")

        self.tw_LopHoc_dsLopHoc.setSortingEnabled(True)
        self.btn_LopHoc_Them.clicked.connect(self.clink_btn_LopHoc_Them)
        self.btn_LopHoc_Sua.clicked.connect(self.clink_btn_LopHoc_Sua)
        self.btn_LopHoc_Xoa.clicked.connect(self.clink_btn_LopHoc_Xoa)
        self.tw_LopHoc_dsLopHoc.cellClicked.connect(self.click_tw_LopHoc_dsLopHoc)
        self.cbb_LopHoc_Nam.currentIndexChanged.connect(self.load_cbb_LopHoc_Nam)
        self.cbb_LopHoc_MaMH.currentIndexChanged.connect(self.load_cbb_LopHoc_MaMH)
        self.cbb_LopHoc_MaGV.currentIndexChanged.connect(self.load_cbb_LopHoc_MaGV)

        self.load()
        self.show()


# pageLOAD
    def load(self):

        dsLop = XLDL.xldl_lop.layDSLop()
        for i in dsLop:#load danh sach lop
            self.cbb_T_lop.addItem(i.getMalop())  # load CBB danh sách lớp TAB THÊM
            self.cbb_LH_lop.addItem(i.getMalop())  # load CBB danh sách lớp TAB danh sách Lớp HỌC
            self.cbb_TK_SV_Lop.addItem(i.getMalop())  # load CBB danh sách lớp TAB Thống kê

        dsNamhoc = XLDL.xldl_NamHoc.layDSNamHoc()
        for i in dsNamhoc:# load nam hoc
            self.cbb_D_NamHoc.addItem(i.getNamHoc())  # load CBB năm học tab DD
            self.cbb_LH_Namhoc.addItem(i.getNamHoc())  # load CBB năm học tab danh sách Lớp học
            self.cbb_TK_LH_NamHoc.addItem(i.getNamHoc())  # load CBB năm học tab Thống kê
            self.cbb_LopHoc_Nam.addItem(i.getNamHoc())  # load CBB năm học tab lớp học

        dsGV = XLDL.xldl_GiangVien.layDSGiangVien()
        for i in dsGV:  # load Giảng viên
            self.cbb_LopHoc_MaGV.addItem(i.getMaGV() + " " + i.getTenGV()) # load CBB giảng viên tab lớp học

        dsMonHoc = XLDL.xldl_MonHoc.layDSMonHoc()
        for i in dsMonHoc:  # load Môn Họ
            self.cbb_LopHoc_MaMH.addItem(i.getMaMH() + " " + i.getTenMH()) # load CBB môn học tab lớp học

# TAB Lớp Học
    def load_cbb_LopHoc_Nam(self):
        QLLopHoc.loadDSLopHoc(self.tw_LopHoc_dsLopHoc, self.cbb_LopHoc_Nam.currentText(), self.cbb_LopHoc_MaGV.currentText())

    def load_cbb_LopHoc_MaMH(self):
        print('click tw ds lớp học')

    def load_cbb_LopHoc_MaGV(self):
        QLLopHoc.loadDSLopHoc(self.tw_LopHoc_dsLopHoc, self.cbb_LopHoc_Nam.currentText(), self.cbb_LopHoc_MaGV.currentText())

    def clink_btn_LopHoc_Them(self):
        malophoc = self.txt_LopHoc_TenLopHoc.text() + self.cbb_LopHoc_Nam.currentText()[-2:]
        if malophoc.find(' ') == -1:
            try:
                thongbao = QLLopHoc.them(malophoc, self.txt_LopHoc_TenLopHoc.text(), self.cbb_LopHoc_Nam.currentText(), self.cbb_LopHoc_MaMH.currentText(), self.cbb_LopHoc_MaGV.currentText(),self.txt_LopHoc_siso.text() )
            except Exception as e:
                thongbao = str(e)
            QMessageBox.about(self, "Thông báo", thongbao)
        else:
            QMessageBox.about(self, "Thông báo", "Tên lớp học phải bao gồm [Mã Môn Học] và [Khối lớp] viết liền không dấu.")
        self.load_cbb_LopHoc_MaGV()

    def clink_btn_LopHoc_Sua(self):
        thongbao = ""
        if self.txt_LopHoc_MaLopHoc.text() != "":
            buttonReply = QMessageBox.question(self, 'Xác nhân chỉnh sửa', "Bạn có chắc chắn chỉnh sửa lớp này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                try:
                    thongbao = QLLopHoc.sua(self.txt_LopHoc_MaLopHoc.text(), self.txt_LopHoc_TenLopHoc.text(), self.cbb_LopHoc_Nam.currentText(),
                                             self.cbb_LopHoc_MaMH.currentText(), self.cbb_LopHoc_MaGV.currentText(),
                                             self.txt_LopHoc_siso.text())
                except Exception as e:
                    thongbao = str(e)
        else:
            thongbao = "Vui lòng chọn lớp học bạn muốn sửa."
        QMessageBox.about(self, "Thông báo", thongbao)
        self.load_cbb_LopHoc_MaGV()

    def clink_btn_LopHoc_Xoa(self):
        thongbao = ""
        if self.txt_LopHoc_MaLopHoc.text() != "":
            buttonReply = QMessageBox.question(self, 'Xác nhân xóa', "Bạn có chắc chắn xóa lớp học này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                try:
                    thongbao = QLLopHoc.xoa(self.txt_LopHoc_MaLopHoc.text())
                except Exception as e:
                    thongbao = str(e)
        else:
            thongbao = "Vui lòng chọn lớp học bạn muốn xóa."
        QMessageBox.about(self, "Thông báo", thongbao)
        self.load_cbb_LopHoc_MaGV()

    def click_tw_LopHoc_dsLopHoc(self):
        print('click')
        row = self.tw_LopHoc_dsLopHoc.currentItem().row()  # lấy row của lớp đc chọn
        malophoc = self.tw_LopHoc_dsLopHoc.item(row, 3)  # lấy mã lớp học
        tenlophoc = self.tw_LopHoc_dsLopHoc.item(row, 4)  # lấy tên lớp học
        siso = self.tw_LopHoc_dsLopHoc.item(row, 5)  # lấy sỉ số
        self.txt_LopHoc_MaLopHoc.setText(malophoc.text())
        self.txt_LopHoc_siso.setText(siso.text())
        self.txt_LopHoc_TenLopHoc.setText(tenlophoc.text().split(' ')[0][:-2])


#TAB Thống kê
    # Tab thống kê theo LỚP HỌC

    def load_TK_LH_NamHoc(self): # CHỌN NĂM HỌC LOAD CONBOBOX LỚP HỌC
        dsLophoc = XLDL.xldl_LopHoc.layDSLopHoc(self.cbb_TK_LH_NamHoc.currentText())
        self.cbb_TK_LH_LopHoc.clear()
        for i in dsLophoc:
            self.cbb_TK_LH_LopHoc.addItem(i.getTenLH())

    def load_TK_LH_LopHoc(self):# CHỌN LỚP HỌC LOAD DS LỚP

        for i in range(self.songay):
            self.tw_TK_LH.removeColumn(6)
        self.songay = QLThongKe.loadDSLopHoc(self.tw_TK_LH, self.cbb_TK_LH_LopHoc.currentText())

        #LOAD THÔNG TIN LỚP HỌC
        ttsinhVien = XLDL.xldl_LopHoc.layThonTinLopHoc(self.cbb_TK_LH_LopHoc.currentText().split(' ')[0])
        try:
            self.txt_TK_LH_Malop.setText(ttsinhVien[0])
            self.txt_TK_HL_TenLop.setText(str(ttsinhVien[1]))
            self.txt_TK_LH_GV.setText(ttsinhVien[2])
            self.txt_TK_LH_siso.setText(str(ttsinhVien[3]))
        except:
            ttlophoc = []
        sum = 0
        for row in range(self.tw_TK_LH.rowCount()):
            sum = sum + int(self.tw_TK_LH.item(row, 4).text())
        self.txt_TK_LH_tongV.setText(str(sum))

    def ds_TK_LH_clicked(self):
        print('click tw ds lớp học')

    # Xuất file excel Lớp học
    def clink_btn_TK_LH_xuat(self):
        print('xuat báo cáo')
        try:
            QLThongKe.xuat_bao_cao(self.tw_TK_LH, self.cbb_TK_LH_LopHoc.currentText(), self.cbb_TK_LH_NamHoc.currentText())
            QMessageBox.about(self, "Thông báo", "Xuất báo cáo thành công")
        except Exception as e:
            print(e)
           # QMessageBox.about(self, "Thông báo", e())

    # xuất biểu đồ Lớp học
    def clink_btn_TK_LH_bieuDo(self):
        try:
            QLThongKe.load_pie(self.tw_TK_LH, 5)
        except Exception as e:
            print(e)

    # Tab thống kê theo SINH VIÊN
    def load_TK_SV_CBBsv(self): # chọn cbb lớp sinh hoạt load cbb danh sách sinh viên
        dsSinhvien = XLDL.xldl_QLSinhVienLopHoc.layDSsinhVienLop(self.cbb_TK_SV_Lop.currentText())
        self.cbb_TK_SV_sv.clear()
        for i in dsSinhvien:
            self.cbb_TK_SV_sv.addItem(i.getmaSV() +" "+ i.getTenSV())

    def load_TK_SV_TWSV(self):
        QLThongKe.loadDSSinhVien(self.tw_TK_SV, self.cbb_TK_SV_sv.currentText())

        # LOAD THÔNG TIN SINH VIÊN
        ttsinhVien = XLDL.xldl_SinhVien.layThonTinSinhVien(self.cbb_TK_SV_sv.currentText().split(' ')[0])
        try:
            self.txt_TK_HS_masv.setText(ttsinhVien[0])
            self.txt_TK_HS_tenSV.setText(ttsinhVien[1])
            self.txt_TK_HS_GioiTinh.setText(ttsinhVien[2])
            self.txt_TK_HS_diaChi.setText(ttsinhVien[3])
        except:
            ttsinhVien = []
        sum = 0
        for row in range(self.tw_TK_SV.rowCount()):
            sum = sum + int(self.tw_TK_SV.item(row, 3).text())
        self.txt_TK_HS_TongV.setText(str(sum))

    def ds_TK_SV_clicked(self):
        print('')

    # Xuất biểu đồ sinh viên
    def clink_btn_TK_HS_bieuDo(self):
        try:
            QLThongKe.load_pie_SV(self.tw_TK_SV)
        except Exception as e:
            print(e)


    # Xuất file excel điểm danh sinh viên
    def clink_btn_TK_SV_xuat(self):
        print('xuat báo cáo')
        try:
            QLThongKe.xuat_bao_cao_SV(self.tw_TK_SV, self.cbb_TK_SV_sv.currentText())
            QMessageBox.about(self, "Thông báo", "Xuất báo cáo thành công")
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Thông báo", e)

#TAB Môn học

    def loadDSMonHoc(self):# load danh sách Môn học lên Table Widget
        QLMonHoc.loadDSMonHoc(self.TW_MH_dsmh)

    def dsMH_clicked(self):
        print('cl')
        row = self.TW_MH_dsmh.currentItem().row()  # lấy row của môn học đc chọn
        maMH = self.TW_MH_dsmh.item(row, 0)  # lấy mã Môn học
        tenMH = self.TW_MH_dsmh.item(row, 1)  # lấy mã Môn học
        SoTC = self.TW_MH_dsmh.item(row, 2)  # lấy mã Môn học
        self.txt_MH_mamh.setText(maMH.text())
        self.txt_MH_tenmh.setText(tenMH.text())
        self.txt_MH_tinchi.setText(SoTC.text())

    def click_btn_MH_them(self):
        print("them mh")
        if self.txt_MH_mamh.text() != '' and self.txt_MH_tenmh.text() != '' and self.txt_MH_tinchi.text() != '':
            thongbao = QLMonHoc.them(self.txt_MH_mamh.text(), self.txt_MH_tenmh.text(), self.txt_MH_tinchi.text())
            self.loadDSMonHoc()
            QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền đầy đủ thông tin môn học!")

    def click_btn_MH_sua(self):
        print("Sua MH")
        if self.txt_MH_mamh.text() != '' and self.txt_MH_tenmh.text() != '' and self.txt_MH_tinchi.text() != '':
            # confirm btn sửa
            buttonReply = QMessageBox.question(self, 'Xác nhân sửa', "Bạn có chắc chắn sửa môn học này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                thongbao = QLMonHoc.sua(self.txt_MH_mamh.text(), self.txt_MH_tenmh.text(), self.txt_MH_tinchi.text())
                self.loadDSMonHoc()
                QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền đầy đủ thông tin môn học!")

    def click_btn_MH_xoa(self):
        print("xoa MH")
        if self.txt_MH_mamh.text() != '' :
            # confirm btn xóa
            buttonReply = QMessageBox.question(self, 'Xác nhân xóa', "Bạn có chắc chắn xóa môn học này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                thongbao = QLMonHoc.xoa(self.txt_MH_mamh.text())
                self.loadDSMonHoc()
                QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền mã môn học bạn muốn xóa!")

#TAB LỚP SINH HOẠT
    def loadDSLopsinhhoat(self):# load danh sách lớp sinh hoat lên Table Widget
        QLLopsinhhoat.loadDSLopsinhhoat(self.TW_L_dsLop)

    def dsLopsinhhoat_clicked(self):
        print('click')
        row = self.TW_L_dsLop.currentItem().row()  # lấy row của lớp đc chọn
        malop = self.TW_L_dsLop.item(row, 0)  # lấy mã lớp
        tenlop = self.TW_L_dsLop.item(row, 1)  # lấy mã lớp
        self.txt_L_malop.setText(malop.text())
        self.txt_L_tenlop.setText(tenlop.text())

    def click_btn_L_them(self):
        print("them lớp sinh hoạt")
        if self.txt_L_malop.text() != '' and self.txt_L_tenlop.text() != '':
            thongbao = QLLopsinhhoat.them(self.txt_L_malop.text(), self.txt_L_tenlop.text())
            self.loadDSLopsinhhoat()
            QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền đầy đủ thông tin lớp!")

    def click_btn_L_xoa(self):
        print("xoa lớp sinh hoạt")
        if self.txt_L_malop.text() != '':
            # confirm btn xóa
            buttonReply = QMessageBox.question(self, 'Xác nhân xóa', "Bạn có chắc chắn xóa lớp này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                thongbao = QLLopsinhhoat.xoa(self.txt_L_malop.text())
                self.loadDSLopsinhhoat()
                QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền mã lớp bạn muốn xóa!")

    def click_btn_L_sua(self):
        print("Sua lớp sinh hoat ")
        if self.txt_L_malop.text() != '' and self.txt_L_tenlop.text() != '':
            # confirm btn sửa
            buttonReply = QMessageBox.question(self, 'Xác nhân sửa', "Bạn có chắc chắn sửa lớp này?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                thongbao = QLLopsinhhoat.sua(self.txt_L_malop.text(), self.txt_L_tenlop.text())
                self.loadDSLopsinhhoat()
                QMessageBox.about(self, "Thông báo", str(thongbao))
        else:
            QMessageBox.about(self, "Thông báo", "Vui lòng điền đầy đủ thông tin lớp !")

#TAB Quản lý SV (Lớp học)

    def load_LH_LopHoc(self):
        dsLophoc = XLDL.xldl_LopHoc.layDSLopHoc(self.cbb_LH_Namhoc.currentText())
        self.cbb_LH_lophoc.clear()
        for i in dsLophoc:
            self.cbb_LH_lophoc.addItem(i.getTenLH())  # load CBB Lớp học TAB Lớp học

    def load_tw_LH_DSLopHoc(self): #load dssv theo lớp học (CS434A)
        self.dsMasvLH.clear()
        QLSinhVien.loadDSSV_LopHoc(self.tw_LH_DSLopHoc, self.cbb_LH_lophoc.currentText())

    def load_tw_LH_DSsv(self): # load dssv theo lớp sinh hoạt (TMP2)
        self.dsMasv.clear()
        QLSinhVien.loadDSSV_Lop(self.tw_LH_DSsv, self.cbb_LH_lop.currentText())

    def clink_btn_LH_tim(self):# click btn tìm
        QLSinhVien.click_btn_tim(self.tw_LH_DSsv, self.txt_LH_timSV.text())

    def clink_btn_LH_Them(self):
        # Thêm sinh viên vào lớp học với các đối số: dsMSV, maLopHoc
        thongbao = QLSinhVien.them(self.dsMasv, self.cbb_LH_lophoc.currentText())
        self.load_tw_LH_DSLopHoc()
        QMessageBox.about(self, "Thông báo", str(thongbao))

    def clink_btn_LH_themALL(self):
        dssv = []
        for row in range(self.tw_LH_DSsv.rowCount()): #tạo danh sách sinh viên có all SV có trong Bảng
            dssv.append(self.tw_LH_DSsv.item(row, 0).text())
        thongbao = QLSinhVien.them(dssv, self.cbb_LH_lophoc.currentText())
        self.load_tw_LH_DSLopHoc()
        QMessageBox.about(self, "Thông báo", str(thongbao))

    def clink_btn_LH_bo(self):
        # Xóa sinh viên vào lớp học với các đối số: dsMSV, maLopHoc
        QLSinhVien.bo(self.dsMasvLH, self.cbb_LH_lophoc.currentText())
        self.load_tw_LH_DSLopHoc()

    def clink_btn_LH_BoALL(self):
        dssv = []
        for row in range(self.tw_LH_DSLopHoc.rowCount()):  # tạo danh sách sinh viên có all SV có trong Bảng
            dssv.append(self.tw_LH_DSLopHoc.item(row, 0).text())
        QLSinhVien.bo(dssv, self.cbb_LH_lophoc.currentText())
        self.load_tw_LH_DSLopHoc()

    def dsLH_clicked(self):
        row = self.tw_LH_DSLopHoc.currentItem().row()  # lấy row của SV đc chọn
        masv = self.tw_LH_DSLopHoc.item(row, 0)  # lấy mã sinh viên
        if self.dsMasvLH.count(masv.text()) == 0:  # Đếm masv có trong dsMasv == 0 thì ..
            self.dsMasvLH.append(masv.text())  # Thêm masv vào trong dsMasv
            masv.setCheckState(QtCore.Qt.Checked)  # Check
        else:
            self.dsMasvLH.remove(masv.text())  # Xóa masv trong dsMasv
            masv.setCheckState(QtCore.Qt.Unchecked)  # Un Check
        print(self.dsMasvLH)

    def dsSV_clicked(self):
        row = self.tw_LH_DSsv.currentItem().row()   # lấy row của SV đc chọn
        masv = self.tw_LH_DSsv.item(row, 0)    # lấy mã sinh viên
        if self.dsMasv.count(masv.text()) == 0:  # Đếm masv có trong dsMasv == 0 thì ..
            self.dsMasv.append(masv.text())     # Thêm masv vào trong dsMasv
            masv.setCheckState(QtCore.Qt.Checked) # Check
        else:
            self.dsMasv.remove(masv.text())     #Xóa masv trong dsMasv
            masv.setCheckState(QtCore.Qt.Unchecked) # Un Check
        print(self.dsMasv)


        # load danh sách sinh viên

    def load_DD_LopHoc(self):
        dsLophoc = XLDL.xldl_LopHoc.layDSLopHoc(self.cbb_D_NamHoc.currentText())
        self.cbb_D_Lophoc.clear()
        for i in dsLophoc:
            self.cbb_D_Lophoc.addItem(i.getTenLH())  # load CBB Lớp học TAB DD



    #load sinh viên theo CBB
    def loadSV(self):
        # load danh sách sinh viên
        malophoc = self.cbb_D_Lophoc.currentText()

        self.DT_D_NgayDD.setDisplayFormat('MM.dd.yyyy   AP')
        ngaydd = self.DT_D_NgayDD.dateTime().toString(self.DT_D_NgayDD.displayFormat())
        ap = ngaydd[-2:]
        ngaydd = ngaydd.split(' ')[0]
        print('ap= ',ap)
        if ap=='AM':
            ngaydd = ngaydd + " 9:00"
        else:
            ngaydd = ngaydd + " 15:00"
        print(ngaydd)
        dsSinhVien = XLDL.xldl_SinhVien.layDSsinhVien(malophoc.split(' ')[0], ngaydd)
        row = 0
        try:
            self.TW_D_dsSV.setRowCount(len(dsSinhVien))
        except Exception as e:
            print(e)
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
                scaleFactor=1.12,
                minNeighbors=5,
                minSize=(30, 30)
                # flags=cv2.CV_HAAR_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 228, 220), 2)
                roi_gray = gray[y:y + h, x:x + w]
                id, confidence = recognizer.predict(roi_gray)

                if confidence < 40:
                    profile = self.getprofile(id)
                    if (profile != None):
                        cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                        print('pro= ', profile)
                        malophoc = self.cbb_D_Lophoc.currentText()
                        self.DT_D_NgayDD.setDisplayFormat('MM.dd.yyyy   AP')
                        ngaydd = self.DT_D_NgayDD.dateTime().toString(self.DT_D_NgayDD.displayFormat())
                        ap = ngaydd[-2:]
                        ngaydd = ngaydd.split(' ')[0]
                        print('ap= ', ap)
                        if ap == 'AM':
                            ngaydd = ngaydd + " 9:00"
                        else:
                            ngaydd = ngaydd + " 15:00"

                        conn = DataConn.DBConnet.getConnet()
                        query = "SELECT * FROM Diemdanh WHERE malophoc='" + malophoc.split(' ')[0] + "' and masv='"+profile[0]+"' and ngaydd='"+ngaydd+"'"
                        cursor = conn.execute(query)

                        isRecordExits = 0

                        for row in cursor:
                            isRecordExits = 1
                        if (isRecordExits == 0):
                            query = "insert into Diemdanh values ('"+malophoc.split(' ')[0]+"', '"+profile[0]+"', '"+ngaydd+"', 'True' )"
                            print('them')
                            print(query)
                            try:
                                conn.execute(query)
                            except Exception as e:
                                print(e)
                        else:
                            query = "update Diemdanh set vang = 'True'  WHERE malophoc='" + malophoc.split(' ')[0] + "' and masv='"+profile[0]+"' and ngaydd='"+ngaydd+"'"
                            print('up')
                            print(query)
                            try:
                                conn.execute(query)
                            except Exception as e:
                                print(e)

                        conn.commit()
                        conn.close()

                        """qery = "insert into Diemdanh values ('"+malophoc.split(' ')[0]+"', '"+profile[0]+"', '"+ngaydd+"', 'True' )"

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
                scaleFactor=1.12,
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
                    cv2.imwrite('dataSet/sv.' + str(self.txt_T_masv.text()).lower().split('sv')[1] + '.' + str(sampleNum) + '.jpg', gray[y: y + h, x: x + w])
                #đưa ảnh đã chụp lên laybel hình ở tab thêm
                    #self.displayImageLAYBEL(gray[y: y + h, x: x + w], self.label_T_hinh, 1)
                    self.label_T_hinh.setPixmap(QPixmap('dataSet/sv.' + str(self.txt_T_masv.text()).lower().split('sv')[1] + '.' + str(sampleNum) + '.jpg'))
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
                                  f.split('.')[1] == self.txt_T_masv.text().lower().split('sv')[1]]
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
        imagePaths = [os.path.join('dataSet', f) for f in os.listdir('dataSet') if f.split('.')[1] == masv.lower().split('sv')[1]]
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
