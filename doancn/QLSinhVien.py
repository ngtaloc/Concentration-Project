from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

import DataConn
from Controllers import XLDL



def loadDSSV_LopHoc(TW_dsSV, malophoc ):
    # load danh sách sinh viên theo mã lớp học CS434A


    dsSinhVien = XLDL.xldl_QLSinhVienLopHoc.layDSsinhVien(malophoc.split(' ')[0])
    row = 0
    TW_dsSV.setRowCount(len(dsSinhVien))

    for sv in dsSinhVien:
        TW_dsSV.setItem(row, 0, QTableWidgetItem(sv.getmaSV()))
        TW_dsSV.setItem(row, 1, QTableWidgetItem(sv.getTenSV()))
        TW_dsSV.setItem(row, 2, QTableWidgetItem(sv.getgioitinh()))
        TW_dsSV.setItem(row, 3, QTableWidgetItem(sv.getdiachi()))
        row = row +1

def loadDSSV_Lop(TW_dsSV, malop):
    # load danh sách sinh viên theo lớp TPM2

    dsSinhVien = XLDL.xldl_QLSinhVienLopHoc.layDSsinhVienLop(malop)
    row = 0
    TW_dsSV.setRowCount(len(dsSinhVien))

    for sv in dsSinhVien:
        TW_dsSV.setItem(row, 0, QTableWidgetItem(sv.getmaSV()))
        TW_dsSV.setItem(row, 1, QTableWidgetItem(sv.getTenSV()))
        TW_dsSV.setItem(row, 2, QTableWidgetItem(sv.getgioitinh()))
        TW_dsSV.setItem(row, 3, QTableWidgetItem(sv.getdiachi()))

        row = row + 1

def click_btn_tim(TW_dsSV, tim):
    # Tìm sinh viên

    dsSinhVien = XLDL.xldl_QLSinhVienLopHoc.TimSV(tim)
    row = 0
    TW_dsSV.setRowCount(len(dsSinhVien))

    for sv in dsSinhVien:
        TW_dsSV.setItem(row, 0, QTableWidgetItem(sv.getmaSV()))
        TW_dsSV.setItem(row, 1, QTableWidgetItem(sv.getTenSV()))
        TW_dsSV.setItem(row, 2, QTableWidgetItem(sv.getgioitinh()))
        TW_dsSV.setItem(row, 3, QTableWidgetItem(sv.getdiachi()))

        row = row + 1

def them(dsMSV, maLopHoc):
    print(dsMSV)
    print(maLopHoc)
    t=0; l=0
    conn = DataConn.DBConnet.getConnet()
    for msv in dsMSV:
        query = "INSERT INTO CTLopHoc VALUES ('"+maLopHoc.split(' ')[0]+"', '"+msv+"')"
        try:
            conn.execute(query)
            conn.commit()
            t=t+1
        except:
            l=l+1

        dsNgay = XLDL.xldl_ThongKe.layDSngayDD(maLopHoc.split(' ')[0])
        for i in range(len(dsNgay)):
            try:
                query = "SELECT * FROM Diemdanh WHERE malophoc='" + maLopHoc.split(' ')[
                    0] + "' and masv='" + msv + "' and ngaydd='" + str(dsNgay[i]) + "'"
                cursor = conn.execute(query)
                isRecordExits = 0
                for rowT in cursor:
                    isRecordExits = 1
                if (isRecordExits == 0):
                    query = "insert into Diemdanh values ('" + maLopHoc.split(' ')[0] + "', '" + msv + "', '" + str(dsNgay[i]) + "', 'False' )"
                    try:
                        conn.execute(query)
                    except Exception as e:
                        print(e)
                conn.commit()
            except Exception as e:
                print(e)

    conn.close()
    st = 'Đã thêm '+ str(t) +' Sinh viên, và có '+str(l)+' sinh viên bị trùng'
    return st

def bo(dsMSV, maLopHoc):
    print('bo')
    conn = DataConn.DBConnet.getConnet()
    for msv in dsMSV:
        query = "Delete FROM CTLopHoc WHERE maLopHoc='" + maLopHoc.split(' ')[0] + "' and masv='" + msv + "'"
        conn.execute(query)


        dsNgay = XLDL.xldl_ThongKe.layDSngayDD(maLopHoc.split(' ')[0])
        for i in range(len(dsNgay)):
            try:
                query = "delete from Diemdanh WHERE malophoc='" + maLopHoc.split(' ')[0] + "' and masv='" + msv + "' and ngaydd='" + str(dsNgay[i]) + "'"
                conn.execute(query)
            except Exception as e:
                print(e)
    conn.commit()
    conn.close()


