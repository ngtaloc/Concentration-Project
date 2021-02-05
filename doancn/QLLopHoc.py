from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import DataConn
from Controllers import XLDL



def loadDSLopHoc(tw_dsLH, namHoc, giangVien ):
    # load danh sách Lớp học theo năm học và giảng viên
    dsLopHoc = XLDL.xldl_LopHoc.layDSLopHoc_nam_gv(namHoc.split(' ')[0], giangVien.split(' ')[0])
    row = 0
    tw_dsLH.setRowCount(len(dsLopHoc))

    for lh in dsLopHoc:
        tw_dsLH.setItem(row, 0, QTableWidgetItem(lh.getMaGV()))
        tw_dsLH.setItem(row, 1, QTableWidgetItem(lh.getMaMH()))
        tw_dsLH.setItem(row, 2, QTableWidgetItem(lh.getNamHoc()))
        tw_dsLH.setItem(row, 3, QTableWidgetItem(lh.getMaLopH()))
        tw_dsLH.setItem(row, 4, QTableWidgetItem(lh.getTenLH()))
        tw_dsLH.setItem(row, 5, QTableWidgetItem(str(lh.getSiSo())))
        row = row +1

def click_btn_tim(tw_dsLH, tim):
    # Tìm sinh viên

    dsLopHoc = XLDL.xldl_QLSinhVienLopHoc.TimSV(tim)
    row = 0
    tw_dsLH.setRowCount(len(dsLopHoc))

    for sv in dsLopHoc:
        tw_dsLH.setItem(row, 0, QTableWidgetItem(sv.getmaSV()))
        tw_dsLH.setItem(row, 1, QTableWidgetItem(sv.getTenSV()))
        tw_dsLH.setItem(row, 2, QTableWidgetItem(sv.getgioitinh()))
        tw_dsLH.setItem(row, 3, QTableWidgetItem(sv.getdiachi()))

        row = row + 1

def them(maLopHoc, tenLopHoc, nam, maMH, maGV, siso):
    conn = DataConn.DBConnet.getConnet()
    query = "INSERT INTO LopHoc VALUES ('"+maLopHoc.split(' ')[0]+"', N'"+tenLopHoc+"','"+nam+"', '"+maMH.split(' ')[0]+"','"+maGV.split(' ')[0]+"',"+siso+")"
    try:
        conn.execute(query)
        conn.commit()
        st = 'Đã thêm thành công'
    except Exception as e:
        print(e)
        st = "Lớp học này đã có rồi!"
    conn.close()

    return st


def xoa(maLopHoc):
    conn = DataConn.DBConnet.getConnet()
    query = " DELETE FROM LopHoc WHERE maLopHoc = '"+maLopHoc+"';"

    try:
        conn.execute(query)
        conn.commit()
        st = 'Xóa thành công !'
    except Exception as e:
        print(e)
        st = str(e)
    conn.close()
    return st

def sua(maLopHoc, tenLopHoc, nam, maMH, maGV, siso):
    conn = DataConn.DBConnet.getConnet()
    query = " UPDATE LopHoc SET tenLop = N'"+tenLopHoc+"', Nam = '"+nam+"', maMH = '"+maMH.split(' ')[0]+"', maGV = '"+maGV.split(' ')[0]+"', siso = "+siso+"  WHERE maLopHoc = '"+maLopHoc.split(' ')[0]+"';"

    try:
        conn.execute(query)
        conn.commit()
        st = 'Sửa thành công !'
    except Exception as e:
        print(e)
        st = str(e)

    conn.close()
    return st


