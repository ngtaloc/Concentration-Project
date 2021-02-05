from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

import DataConn
from Controllers import XLDL

def loadDSLopsinhhoat(TW_L_dsLop ):
    dsLopsinhhoat = XLDL.xldl_lop.layDSLop()
    row = 0
    TW_L_dsLop.setRowCount(len(dsLopsinhhoat))

    for lopsh in dsLopsinhhoat:
        TW_L_dsLop.setItem(row, 0, QTableWidgetItem(lopsh.getMalop()))
        TW_L_dsLop.setItem(row, 1, QTableWidgetItem(lopsh.getTenLop()))
        row = row +1


def them(malop, tenlop):
    conn = DataConn.DBConnet.getConnet()
    query = "INSERT INTO Lop VALUES ('"+malop+"', N'"+tenlop+"')"
    st = 'Thêm thành công !'
    try:
        conn.execute(query)
        conn.commit()
    except Exception as e:
        if str(e).find('PRIMARY KEY') !=-1:
            st = 'Mã lớp học này đã có rồi.'
            print(e)
    conn.close()

    return st
def xoa(maLop):
    conn = DataConn.DBConnet.getConnet()
    query = " DELETE FROM Lop WHERE maLop = '"+maLop+"';"
    st = 'Xóa thành công !'
    try:
        conn.execute(query)
        conn.commit()
        print(query)
    except Exception as e:
        return e
    conn.close()

    return st

def sua(maLop,tenLop):
    conn = DataConn.DBConnet.getConnet()
    query = " UPDATE Lop SET tenLop = N'"+tenLop+"'  WHERE maLop = '"+maLop+"';"
    st = 'Sửa thành công !'
    try:
        conn.execute(query)
        conn.commit()
        print(query)
    except Exception as e:
        return e
    conn.close()
    return st

